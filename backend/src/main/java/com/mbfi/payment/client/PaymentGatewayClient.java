package com.mbfi.payment.client;

public interface PaymentGatewayClient {
    GatewayPayment confirm(String paymentKey, String orderId, long amount);
    GatewayPayment get(String paymentKey);
    GatewayCancellation cancel(String paymentKey, String reason, long amount);

    record GatewayPayment(String paymentKey, String orderId, long totalAmount, String status) {
    }

    record GatewayCancellation(String transactionKey, long canceledAmount, String status) {
    }
}
