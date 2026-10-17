package com.mbfi.payment.client;

import java.nio.charset.StandardCharsets;
import java.util.Base64;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class TossPaymentsClient implements PaymentGatewayClient {
    private final RestClient client;
    private final String secretKey;

    public TossPaymentsClient(
            @Value("${app.payment.toss-base-url}") String baseUrl,
            @Value("${app.payment.toss-secret-key:}") String secretKey
    ) {
        this.client = RestClient.builder()
                .baseUrl(baseUrl)
                .defaultHeaders(headers -> headers.setBasicAuth(encodedSecretKey(secretKey)))
                .build();
        this.secretKey = secretKey;
    }

    @Override
    public GatewayPayment confirm(String paymentKey, String orderId, long amount) {
        requireConfigured();

        TossPaymentResponse response = client.post()
                .uri("/v1/payments/confirm")
                .contentType(MediaType.APPLICATION_JSON)
                .body(new ConfirmRequest(paymentKey, orderId, amount))
                .retrieve()
                .body(TossPaymentResponse.class);

        return response.toGatewayPayment();
    }

    @Override
    public GatewayPayment get(String paymentKey) {
        requireConfigured();

        TossPaymentResponse response = client.get()
                .uri("/v1/payments/{paymentKey}", paymentKey)
                .retrieve()
                .body(TossPaymentResponse.class);

        return response.toGatewayPayment();
    }

    @Override
    public GatewayCancellation cancel(String paymentKey, String reason, long amount) {
        requireConfigured();

        TossCancelResponse response = client.post()
                .uri("/v1/payments/{paymentKey}/cancel", paymentKey)
                .contentType(MediaType.APPLICATION_JSON)
                .body(new CancelRequest(reason, amount))
                .retrieve()
                .body(TossCancelResponse.class);

        return new GatewayCancellation(
                response.transactionKey(),
                response.canceledAmount(),
                response.status()
        );
    }

    private String encodedSecretKey(String key) {
        String credentials = key + ":";
        return Base64.getEncoder().encodeToString(credentials.getBytes(StandardCharsets.UTF_8));
    }

    private void requireConfigured() {
        if (secretKey.isBlank()) {
            throw new IllegalStateException("TOSS_SECRET_KEY가 설정되지 않았습니다.");
        }
    }

    private record ConfirmRequest(String paymentKey, String orderId, long amount) {
    }

    private record CancelRequest(String cancelReason, long cancelAmount) {
    }

    private record TossPaymentResponse(
            String paymentKey,
            String orderId,
            long totalAmount,
            String status
    ) {
        private GatewayPayment toGatewayPayment() {
            return new GatewayPayment(paymentKey, orderId, totalAmount, status);
        }
    }

    private record TossCancelResponse(String transactionKey, long canceledAmount, String status) {
    }
}
