package com.mbfi.global.exception;

import com.mbfi.global.response.ErrorResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingRequestHeaderException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusiness(BusinessException exception) {
        ErrorCode code = exception.errorCode();
        ErrorResponse response = ErrorResponse.of(code.name(), code.safeMessage());
        return ResponseEntity.status(code.status()).body(response);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ErrorResponse> handleBadRequest(IllegalArgumentException exception) {
        return error(ErrorCode.INVALID_REQUEST);
    }

    @ExceptionHandler(IllegalStateException.class)
    public ResponseEntity<ErrorResponse> handleConflict(IllegalStateException exception) {
        return error(ErrorCode.INVALID_STATE);
    }

    @ExceptionHandler({MethodArgumentNotValidException.class, HttpMessageNotReadableException.class})
    public ResponseEntity<ErrorResponse> handleValidation(Exception exception) {
        return error(ErrorCode.INVALID_REQUEST);
    }

    @ExceptionHandler(MissingRequestHeaderException.class)
    public ResponseEntity<ErrorResponse> handleMissingHeader(MissingRequestHeaderException exception) {
        ErrorCode errorCode = "X-Access-Token".equalsIgnoreCase(exception.getHeaderName())
                ? ErrorCode.UNAUTHORIZED
                : ErrorCode.INVALID_REQUEST;
        return error(errorCode);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpected(Exception exception) {
        return error(ErrorCode.INTERNAL_SERVER_ERROR);
    }

    private ResponseEntity<ErrorResponse> error(ErrorCode errorCode) {
        ErrorResponse response = ErrorResponse.of(errorCode.name(), errorCode.safeMessage());
        return ResponseEntity.status(errorCode.status()).body(response);
    }
}
