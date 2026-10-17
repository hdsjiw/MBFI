package com.mbfi.payment.dto;

public record ConfirmPaymentRequest(String orderId, String paymentKey, long amount) {
}
