package com.mbfi.ai.controller;

import com.mbfi.ai.client.AiClient;
import com.mbfi.global.response.ApiResponse;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/internal/ai")
public class AiProxyController {
    private final AiClient aiClient;

    public AiProxyController(AiClient aiClient) {
        this.aiClient = aiClient;
    }

    @GetMapping("/health")
    public ApiResponse<Map<?, ?>> health() {
        return ApiResponse.success(aiClient.health());
    }
}
