package com.mbfi.global.response;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

class ApiResponseTest {
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Test
    void serializesSuccessResponse() throws Exception {
        String json = objectMapper.writeValueAsString(
                ApiResponse.success(java.util.Map.of("id", "result-1"))
        );
        var tree = objectMapper.readTree(json);

        assertEquals("true", tree.path("success").asText());
        assertEquals("result-1", tree.path("data").path("id").asText());
    }

    @Test
    void serializesErrorResponseWithoutInternalDetails() throws Exception {
        String json = objectMapper.writeValueAsString(
                ErrorResponse.of("PAYMENT_PROVIDER_ERROR", "결제 승인 처리에 실패했습니다.")
        );
        var tree = objectMapper.readTree(json);
        assertEquals("false", tree.path("success").asText());
        assertEquals("PAYMENT_PROVIDER_ERROR", tree.path("code").asText());
        assertEquals("결제 승인 처리에 실패했습니다.", tree.path("message").asText());
    }
}
