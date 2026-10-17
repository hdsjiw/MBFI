package com.mbfi.global.exception;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class GlobalExceptionHandlerTest {
    @Test
    void mapsPaymentAmountMismatchToConflictAndStableCode() {
        var exception = new BusinessException(ErrorCode.PAYMENT_AMOUNT_MISMATCH);
        var response = new GlobalExceptionHandler().handleBusiness(exception);
        assertEquals(409, response.getStatusCode().value());
        assertEquals("PAYMENT_AMOUNT_MISMATCH", response.getBody().code());
        assertEquals(false, response.getBody().success());
    }

    @Test
    void hidesProviderExceptionDetails() {
        var exception = new BusinessException(
                ErrorCode.PAYMENT_PROVIDER_ERROR,
                new RuntimeException("secret-key")
        );
        var response = new GlobalExceptionHandler().handleBusiness(exception);
        assertEquals("결제 승인 처리에 실패했습니다.", response.getBody().message());
    }
}
