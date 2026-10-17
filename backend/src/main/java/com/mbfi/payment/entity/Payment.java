package com.mbfi.payment.entity;

import com.mbfi.global.entity.BaseTimeEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "payment")
public class Payment extends BaseTimeEntity {
    @Id private UUID id;
    @Column(nullable = false) private UUID testResultId;
    @Column(nullable = false, unique = true) private String orderId;
    @Column(unique = true) private String paymentKey;
    @Column(nullable = false) private long amount;
    @Enumerated(EnumType.STRING) @Column(nullable = false) private PaymentStatus status;
    @Column(nullable = false, unique = true) private String idempotencyKey;
    private Instant approvedAt;

    protected Payment() {
    }

    public Payment(
            UUID id,
            UUID testResultId,
            String orderId,
            long amount,
            String idempotencyKey
    ) {
        this.id = id;
        this.testResultId = testResultId;
        this.orderId = orderId;
        this.amount = amount;
        this.idempotencyKey = idempotencyKey;
        this.status = PaymentStatus.READY;
    }

    public UUID getId() {
        return id;
    }

    public UUID getTestResultId() {
        return testResultId;
    }

    public String getOrderId() {
        return orderId;
    }

    public String getPaymentKey() {
        return paymentKey;
    }

    public long getAmount() {
        return amount;
    }

    public PaymentStatus getStatus() {
        return status;
    }

    public String getIdempotencyKey() {
        return idempotencyKey;
    }

    public Instant getApprovedAt() {
        return approvedAt;
    }

    public void beginConfirming(String paymentKey) {
        this.paymentKey = paymentKey;
        status = PaymentStatus.CONFIRMING;
    }

    public void confirm(String paymentKey, Instant now) {
        this.paymentKey = paymentKey;
        status = PaymentStatus.DONE;
        approvedAt = now;
    }

    public void markUnknown() {
        status = PaymentStatus.UNKNOWN;
    }

    public void markFailed() {
        status = PaymentStatus.FAILED;
    }

    public void beginCanceling() {
        status = PaymentStatus.CANCELLING;
    }

    public void canceled() {
        status = PaymentStatus.CANCELED;
    }

    public void partiallyCanceled() {
        status = PaymentStatus.PARTIAL_CANCELED;
    }

    public void cancelFailed() {
        status = PaymentStatus.DONE;
    }
}
