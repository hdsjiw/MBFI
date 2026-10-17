package com.mbfi.payment.dto;

import com.mbfi.payment.entity.Payment;
import java.util.UUID;

public record PaymentResponse(
        UUID id,
        UUID testResultId,
        String orderId,
        long amount,
        String status,
        String paymentKey,
        String approvedAt
) {
    public static PaymentResponse from(Payment payment) {
        String approvedAt = payment.getApprovedAt() == null
                ? null
                : payment.getApprovedAt().toString();
        return new PaymentResponse(
                payment.getId(),
                payment.getTestResultId(),
                payment.getOrderId(),
                payment.getAmount(),
                payment.getStatus().name(),
                payment.getPaymentKey(),
                approvedAt
        );
    }
}
