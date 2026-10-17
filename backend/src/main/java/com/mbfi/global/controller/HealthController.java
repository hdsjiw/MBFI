package com.mbfi.global.controller;

import com.mbfi.global.response.ApiResponse;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {
    @GetMapping("/health")
    public ApiResponse<Map<String, String>> health() {
        Map<String, String> health = Map.of("status", "UP", "service", "backend");
        return ApiResponse.success(health);
    }
}
