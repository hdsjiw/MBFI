package com.mbfi.api;

import java.time.Instant;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {
    @ExceptionHandler(Exception.class)
    public Map<String, Object> handleUnexpected(Exception exception) {
        return Map.of("timestamp", Instant.now().toString(), "status", HttpStatus.INTERNAL_SERVER_ERROR.value(),
                "error", "INTERNAL_SERVER_ERROR", "message", "Unexpected server error");
    }
}
