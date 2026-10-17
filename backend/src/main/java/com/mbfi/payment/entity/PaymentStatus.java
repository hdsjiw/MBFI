package com.mbfi.payment.entity;

public enum PaymentStatus {
    READY,
    CONFIRMING,
    UNKNOWN,
    DONE,
    FAILED,
    CANCELLING,
    CANCELED,
    PARTIAL_CANCELED
}
