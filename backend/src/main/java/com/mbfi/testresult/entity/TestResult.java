package com.mbfi.testresult.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "test_result")
public class TestResult {
    @Id private UUID id;
    @Column(nullable = false, columnDefinition = "TEXT") private String answers;
    @Column(nullable = false) private String financialType;
    @Column(nullable = false, columnDefinition = "TEXT") private String analysisResult;
    @Column(nullable = false) private String algorithmVersion;
    @Column(nullable = false, length = 64) private String accessTokenHash;
    @Column(nullable = false) private Instant accessTokenExpiresAt;
    @Column(nullable = false) private Instant createdAt;

    protected TestResult() {
    }

    public TestResult(
            UUID id,
            String answers,
            String financialType,
            String analysisResult,
            String algorithmVersion,
            String accessTokenHash,
            Instant accessTokenExpiresAt,
            Instant createdAt
    ) {
        this.id = id;
        this.answers = answers;
        this.financialType = financialType;
        this.analysisResult = analysisResult;
        this.algorithmVersion = algorithmVersion;
        this.accessTokenHash = accessTokenHash;
        this.accessTokenExpiresAt = accessTokenExpiresAt;
        this.createdAt = createdAt;
    }

    public UUID getId() {
        return id;
    }

    public String getAnswers() {
        return answers;
    }

    public String getFinancialType() {
        return financialType;
    }

    public String getAnalysisResult() {
        return analysisResult;
    }

    public String getAlgorithmVersion() {
        return algorithmVersion;
    }

    public String getAccessTokenHash() {
        return accessTokenHash;
    }

    public Instant getAccessTokenExpiresAt() {
        return accessTokenExpiresAt;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }
}
