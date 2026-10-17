package com.mbfi.payment.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "payment_cancel")
public class PaymentCancel {
    @Id private UUID id;
    @Column(nullable = false) private UUID paymentId;
    @Column(nullable = false, unique = true) private String idempotencyKey;
    @Column(unique = true) private String pgTransactionKey;
    @Column(nullable = false) private long cancelAmount;
    @Column(nullable = false) private String reason;
    @Enumerated(EnumType.STRING) @Column(nullable = false) private CancelStatus status;
    @Column(nullable = false) private Instant requestedAt;
    private Instant canceledAt;

    protected PaymentCancel() {
    }

    public PaymentCancel(
            UUID id,
            UUID paymentId,
            String idempotencyKey,
            long cancelAmount,
            String reason,
            Instant now
    ) {
        this.id = id;
        this.paymentId = paymentId;
        this.idempotencyKey = idempotencyKey;
        this.cancelAmount = cancelAmount;
        this.reason = reason;
        this.status = CancelStatus.REQUESTED;
        this.requestedAt = now;
    }

    public UUID getId() {
        return id;
    }

    public UUID getPaymentId() {
        return paymentId;
    }

    public String getIdempotencyKey() {
        return idempotencyKey;
    }

    public long getCancelAmount() {
        return cancelAmount;
    }

    public String getReason() {
        return reason;
    }

    public CancelStatus getStatus() {
        return status;
    }

    public String getPgTransactionKey() {
        return pgTransactionKey;
    }

    public Instant getRequestedAt() {
        return requestedAt;
    }

    public Instant getCanceledAt() {
        return canceledAt;
    }

    public void done(String transactionKey, Instant now) {
        status = CancelStatus.DONE;
        pgTransactionKey = transactionKey;
        canceledAt = now;
    }

    public void failed() {
        status = CancelStatus.FAILED;
    }
}
