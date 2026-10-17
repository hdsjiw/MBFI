package com.mbfi.payment.client;

public class FakePaymentGatewayClient implements PaymentGatewayClient {
    public int confirmCalls;
    public int cancelCalls;
    public boolean timeout;
    @Override
    public GatewayPayment confirm(String paymentKey, String orderId, long amount) {
        confirmCalls++;
        if (timeout) {
            throw new org.springframework.web.client.ResourceAccessException("fake timeout");
        }
        return new GatewayPayment(paymentKey, orderId, amount, "DONE");
    }

    @Override
    public GatewayPayment get(String paymentKey) {
        return new GatewayPayment(paymentKey, "MBFI-recovered", 9900, "DONE");
    }

    @Override
    public GatewayCancellation cancel(String paymentKey, String reason, long amount) {
        cancelCalls++;
        return new GatewayCancellation("tx-1", amount, "DONE");
    }
}
