package com.mbfi.report.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "report")
public class Report {
    @Id private UUID id;
    @Column(nullable = false, unique = true) private UUID testResultId;
    @Enumerated(EnumType.STRING) @Column(nullable = false) private ReportStatus status;
    private String storageKey;
    @Column(nullable = false) private Instant createdAt;
    private Instant generatedAt;

    protected Report() {
    }

    public Report(UUID id, UUID testResultId, Instant createdAt) {
        this.id = id;
        this.testResultId = testResultId;
        this.status = ReportStatus.PENDING;
        this.createdAt = createdAt;
    }

    public UUID getId() {
        return id;
    }

    public UUID getTestResultId() {
        return testResultId;
    }

    public ReportStatus getStatus() {
        return status;
    }

    public String getStorageKey() {
        return storageKey;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public Instant getGeneratedAt() {
        return generatedAt;
    }

    public void markFailed() {
        status = ReportStatus.FAILED;
    }
}
