package com.mbfi.payment.service;

import com.mbfi.global.exception.BusinessException;
import com.mbfi.global.exception.ErrorCode;
import com.mbfi.payment.client.PaymentGatewayClient;
import com.mbfi.payment.entity.CancelStatus;
import com.mbfi.payment.entity.Payment;
import com.mbfi.payment.entity.PaymentStatus;
import com.mbfi.testresult.service.TestAnalysisService;
import java.util.UUID;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClientResponseException;

@Service
public class PaymentService {
    private final TestAnalysisService results;
    private final PaymentStateService states;
    private final PaymentGatewayClient gateway;
    private final long reportAmount;

    public PaymentService(TestAnalysisService results, PaymentStateService states, PaymentGatewayClient gateway,
            @Value("${app.payment.amount}") long reportAmount) {
        this.results = results;
        this.states = states;
        this.gateway = gateway;
        this.reportAmount = reportAmount;
    }

    @Transactional
    public Payment create(UUID resultId, String accessToken, String idempotencyKey) {
        results.getAuthorized(resultId, accessToken);
        if (idempotencyKey == null || idempotencyKey.isBlank()) {
            throw new BusinessException(ErrorCode.IDEMPOTENCY_KEY_REQUIRED);
        }
        String orderId = "MBFI-" + UUID.randomUUID();
        return states.create(resultId, orderId, reportAmount, idempotencyKey);
    }

    public Payment confirm(String orderId, String paymentKey, long amount) {
        Payment existing = states.find(orderId);
        if (existing.getStatus() == PaymentStatus.DONE) return states.beginConfirm(orderId, paymentKey, amount);
        states.beginConfirm(orderId, paymentKey, amount);
        try {
            PaymentGatewayClient.GatewayPayment response = gateway.confirm(paymentKey, orderId, amount);
            PaymentStateService.PaymentGatewayResult gatewayResult =
                    new PaymentStateService.PaymentGatewayResult(
                            response.paymentKey(),
                            response.orderId(),
                            response.totalAmount(),
                            response.status()
                    );
            return states.finishConfirm(orderId, paymentKey, gatewayResult);
        } catch (ResourceAccessException exception) {
            states.markUnknown(orderId);
            throw new BusinessException(ErrorCode.PAYMENT_UNKNOWN, exception);
        } catch (RestClientResponseException exception) {
            states.markFailed(orderId);
            throw new BusinessException(ErrorCode.PAYMENT_PROVIDER_ERROR, exception);
        }
    }

    public Payment reconcile(String orderId) {
        Payment payment = states.find(orderId);
        if (payment.getPaymentKey() == null) throw new BusinessException(ErrorCode.PAYMENT_UNKNOWN);
        PaymentGatewayClient.GatewayPayment response = gateway.get(payment.getPaymentKey());
        PaymentStateService.PaymentGatewayResult gatewayResult =
                new PaymentStateService.PaymentGatewayResult(
                        response.paymentKey(),
                        response.orderId(),
                        response.totalAmount(),
                        response.status()
                );
        return states.reconcile(orderId, gatewayResult);
    }

    public Payment authorizedFind(String orderId, String accessToken) {
        Payment payment = states.find(orderId);
        results.getAuthorized(payment.getTestResultId(), accessToken);
        return payment;
    }

    public Payment authorizedReconcile(String orderId, String accessToken) {
        Payment payment = authorizedFind(orderId, accessToken);
        return reconcile(payment.getOrderId());
    }

    public Payment cancel(String orderId, String accessToken, String idempotencyKey, String reason) {
        Payment payment = states.find(orderId);
        results.getAuthorized(payment.getTestResultId(), accessToken);
        var existingCancel = states.findCancel(idempotencyKey);
        if (existingCancel.isPresent() && existingCancel.get().getStatus() == CancelStatus.DONE) return payment;
        states.beginCancel(orderId, idempotencyKey, payment.getAmount(), reason);
        try {
            PaymentGatewayClient.GatewayCancellation response = gateway.cancel(
                    payment.getPaymentKey(),
                    reason,
                    payment.getAmount()
            );
            PaymentStateService.PaymentGatewayCancellation cancellation =
                    new PaymentStateService.PaymentGatewayCancellation(
                            response.transactionKey(),
                            response.canceledAmount(),
                            response.status()
                    );
            return states.finishCancel(orderId, idempotencyKey, cancellation);
        } catch (ResourceAccessException exception) {
            throw new BusinessException(ErrorCode.PAYMENT_UNKNOWN, exception);
        } catch (RestClientResponseException exception) {
            states.failCancel(orderId, idempotencyKey);
            throw new BusinessException(ErrorCode.PAYMENT_CANCEL_FAILED, exception);
        }
    }
}
