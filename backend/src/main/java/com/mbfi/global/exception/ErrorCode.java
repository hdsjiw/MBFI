package com.mbfi.global.exception;

import org.springframework.http.HttpStatus;

public enum ErrorCode {
    INVALID_REQUEST(HttpStatus.BAD_REQUEST, "요청 데이터가 올바르지 않습니다."),
    IDEMPOTENCY_KEY_REQUIRED(HttpStatus.BAD_REQUEST, "Idempotency-Key가 필요합니다."),
    UNAUTHORIZED(HttpStatus.UNAUTHORIZED, "인증이 필요합니다."),
    RESULT_ACCESS_DENIED(HttpStatus.FORBIDDEN, "결과에 접근할 권한이 없습니다."),
    RESOURCE_NOT_FOUND(HttpStatus.NOT_FOUND, "요청한 리소스를 찾을 수 없습니다."),
    INVALID_STATE(HttpStatus.CONFLICT, "현재 상태에서는 요청을 처리할 수 없습니다."),
    PAYMENT_AMOUNT_MISMATCH(HttpStatus.CONFLICT, "결제 금액이 일치하지 않습니다."),
    PAYMENT_ALREADY_COMPLETED(HttpStatus.CONFLICT, "이미 승인 완료된 결제입니다."),
    PAYMENT_ALREADY_CANCELED(HttpStatus.CONFLICT, "이미 취소된 결제입니다."),
    PAYMENT_CONFIRM_IN_PROGRESS(HttpStatus.CONFLICT, "결제 승인이 처리 중입니다."),
    PAYMENT_CANCEL_IN_PROGRESS(HttpStatus.CONFLICT, "결제 취소가 처리 중입니다."),
    PAYMENT_CANCEL_FAILED(HttpStatus.BAD_GATEWAY, "결제 취소에 실패했습니다."),
    PAYMENT_PROVIDER_ERROR(HttpStatus.BAD_GATEWAY, "결제 승인 처리에 실패했습니다."),
    PAYMENT_UNKNOWN(HttpStatus.SERVICE_UNAVAILABLE, "결제 결과가 확인되지 않았습니다. 잠시 후 다시 조회해 주세요."),
    REPORT_NOT_READY(HttpStatus.CONFLICT, "결제 완료 후 리포트를 생성할 수 있습니다."),
    INTERNAL_SERVER_ERROR(HttpStatus.INTERNAL_SERVER_ERROR, "서버 오류가 발생했습니다.");

    private final HttpStatus status;
    private final String safeMessage;
    ErrorCode(HttpStatus status, String safeMessage) {
        this.status = status;
        this.safeMessage = safeMessage;
    }

    public HttpStatus status() {
        return status;
    }

    public String safeMessage() {
        return safeMessage;
    }
}
