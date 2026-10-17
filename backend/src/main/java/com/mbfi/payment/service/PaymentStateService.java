package com.mbfi.payment.service;

import com.mbfi.global.exception.BusinessException;
import com.mbfi.global.exception.ErrorCode;
import com.mbfi.payment.entity.CancelStatus;
import com.mbfi.payment.entity.Payment;
import com.mbfi.payment.entity.PaymentCancel;
import com.mbfi.payment.entity.PaymentStatus;
import com.mbfi.payment.repository.PaymentCancelRepository;
import com.mbfi.payment.repository.PaymentRepository;
import java.time.Instant;
import java.util.Optional;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class PaymentStateService {
    private final PaymentRepository payments;
    private final PaymentCancelRepository cancels;
    public PaymentStateService(PaymentRepository payments, PaymentCancelRepository cancels) {
        this.payments = payments;
        this.cancels = cancels;
    }

    @Transactional
    public Payment create(UUID resultId, String orderId, long amount, String idempotencyKey) {
        Optional<Payment> existing = payments.findByIdempotencyKey(idempotencyKey);
        if (existing.isPresent()) {
            return existing.get();
        }

        Payment payment = new Payment(UUID.randomUUID(), resultId, orderId, amount, idempotencyKey);
        return payments.save(payment);
    }

    @Transactional
    public Payment beginConfirm(String orderId, String paymentKey, long amount) {
        Payment payment = locked(orderId);
        if (payment.getAmount() != amount) {
            throw new BusinessException(ErrorCode.PAYMENT_AMOUNT_MISMATCH);
        }
        if (payment.getStatus() == PaymentStatus.DONE) {
            if (!paymentKey.equals(payment.getPaymentKey())) {
                throw new BusinessException(ErrorCode.PAYMENT_ALREADY_COMPLETED);
            }
            return payment;
        }
        if (payment.getStatus() == PaymentStatus.CONFIRMING) {
            throw new BusinessException(ErrorCode.PAYMENT_CONFIRM_IN_PROGRESS);
        }
        if (payment.getStatus() == PaymentStatus.UNKNOWN) {
            throw new BusinessException(ErrorCode.PAYMENT_UNKNOWN);
        }
        if (payment.getStatus() != PaymentStatus.READY && payment.getStatus() != PaymentStatus.FAILED) {
            throw new BusinessException(ErrorCode.INVALID_STATE);
        }
        payment.beginConfirming(paymentKey);
        return payments.save(payment);
    }

    @Transactional
    public Payment finishConfirm(String orderId, String paymentKey, PaymentGatewayResult gatewayResult) {
        Payment payment = locked(orderId);
        boolean responseMatches = paymentKey.equals(gatewayResult.paymentKey())
                && orderId.equals(gatewayResult.orderId())
                && payment.getAmount() == gatewayResult.amount()
                && "DONE".equals(gatewayResult.status());
        if (!responseMatches) {
            throw new BusinessException(ErrorCode.PAYMENT_PROVIDER_ERROR);
        }
        payment.confirm(paymentKey, Instant.now());
        return payments.save(payment);
    }

    @Transactional
    public Payment markUnknown(String orderId) {
        Payment payment = locked(orderId);
        payment.markUnknown();
        return payments.save(payment);
    }

    @Transactional
    public Payment markFailed(String orderId) {
        Payment payment = locked(orderId);
        payment.markFailed();
        return payments.save(payment);
    }

    @Transactional
    public Payment beginCancel(String orderId, String idempotencyKey, long amount, String reason) {
        Optional<PaymentCancel> existing = cancels.findByIdempotencyKey(idempotencyKey);
        if (existing.isPresent() && existing.get().getStatus() == CancelStatus.DONE) {
            return locked(orderId);
        }
        if (existing.isPresent() && existing.get().getStatus() == CancelStatus.REQUESTED) {
            throw new BusinessException(ErrorCode.PAYMENT_CANCEL_IN_PROGRESS);
        }
        Payment payment = locked(orderId);
        if (payment.getStatus() == PaymentStatus.CANCELED
                || payment.getStatus() == PaymentStatus.PARTIAL_CANCELED) {
            throw new BusinessException(ErrorCode.PAYMENT_ALREADY_CANCELED);
        }
        if (payment.getStatus() != PaymentStatus.DONE || amount != payment.getAmount()) {
            throw new BusinessException(ErrorCode.INVALID_STATE);
        }

        payment.beginCanceling();
        payments.save(payment);
        PaymentCancel cancel = new PaymentCancel(
                UUID.randomUUID(),
                payment.getId(),
                idempotencyKey,
                amount,
                reason,
                Instant.now()
        );
        cancels.save(cancel);
        return payment;
    }

    @Transactional
    public Payment finishCancel(String orderId, String idempotencyKey, PaymentGatewayCancellation result) {
        Payment payment = locked(orderId);
        PaymentCancel cancel = cancels.findByIdempotencyKey(idempotencyKey)
                .orElseThrow(() -> new BusinessException(ErrorCode.RESOURCE_NOT_FOUND));
        if (result.amount() != cancel.getCancelAmount() || !"DONE".equals(result.status())) {
            throw new BusinessException(ErrorCode.PAYMENT_CANCEL_FAILED);
        }

        cancel.done(result.transactionKey(), Instant.now());
        payment.canceled();
        cancels.save(cancel);
        return payments.save(payment);
    }

    @Transactional
    public Payment failCancel(String orderId, String idempotencyKey) {
        Payment payment = locked(orderId);
        cancels.findByIdempotencyKey(idempotencyKey).ifPresent(PaymentCancel::failed);
        payment.cancelFailed();
        return payments.save(payment);
    }

    @Transactional(readOnly = true)
    public Optional<PaymentCancel> findCancel(String idempotencyKey) {
        return cancels.findByIdempotencyKey(idempotencyKey);
    }

    @Transactional(readOnly = true)
    public Payment find(String orderId) {
        return payments.findByOrderId(orderId)
                .orElseThrow(() -> new BusinessException(ErrorCode.RESOURCE_NOT_FOUND));
    }

    @Transactional
    public Payment reconcile(String orderId, PaymentGatewayResult result) {
        return finishConfirm(orderId, result.paymentKey(), result);
    }

    private Payment locked(String orderId) {
        return payments.findByOrderIdForUpdate(orderId)
                .orElseThrow(() -> new BusinessException(ErrorCode.RESOURCE_NOT_FOUND));
    }

    public record PaymentGatewayResult(String paymentKey, String orderId, long amount, String status) {
    }

    public record PaymentGatewayCancellation(String transactionKey, long amount, String status) {
    }
}
