package com.mbfi.api;

import com.mbfi.ai.AiClient;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/internal/ai")
public class AiProxyController {
    private final AiClient aiClient;
    public AiProxyController(AiClient aiClient) { this.aiClient = aiClient; }
    @GetMapping("/health") public Map<?, ?> health() { return aiClient.health(); }
}
