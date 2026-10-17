package com.mbfi.ai.client;

import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class AiClient {
    private final RestClient client;

    public AiClient(@Value("${app.ai-base-url:http://localhost:8000}") String baseUrl) {
        this.client = RestClient.builder()
                .baseUrl(baseUrl)
                .build();
    }

    public Map<?, ?> health() {
        return client.get()
                .uri("/health")
                .retrieve()
                .body(Map.class);
    }
}
