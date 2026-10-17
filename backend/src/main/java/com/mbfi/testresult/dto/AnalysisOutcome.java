package com.mbfi.testresult.dto;

import java.util.UUID;

public record AnalysisOutcome(
        UUID id,
        String accessToken,
        String financialType,
        String analysisResult,
        String algorithmVersion
) {
}
