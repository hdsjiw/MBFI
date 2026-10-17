package com.mbfi.testresult.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.mbfi.global.exception.BusinessException;
import com.mbfi.global.exception.ErrorCode;
import com.mbfi.testresult.dto.AnalysisOutcome;
import com.mbfi.testresult.entity.TestResult;
import com.mbfi.testresult.repository.TestResultRepository;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HexFormat;
import java.util.List;
import java.util.UUID;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class TestAnalysisService {
    private static final String ALGORITHM_VERSION = "v1-placeholder";
    private static final List<String> REQUIRED_QUESTION_IDS = List.of(
            "q1", "q2", "q3", "q4", "q5"
    );
    private final TestResultRepository repository;
    private final ObjectMapper objectMapper;
    private final long accessTokenTtlHours;
    private final SecureRandom secureRandom = new SecureRandom();

    public TestAnalysisService(TestResultRepository repository, ObjectMapper objectMapper,
            @Value("${app.payment.access-token-ttl-hours:24}") long accessTokenTtlHours) {
        this.repository = repository;
        this.objectMapper = objectMapper;
        this.accessTokenTtlHours = accessTokenTtlHours;
    }

    @Transactional
    public AnalysisOutcome analyze(JsonNode answers) {
        validateAnswers(answers);
        try {
            UUID id = UUID.randomUUID();
            String accessToken = randomToken();
            String answersJson = objectMapper.writeValueAsString(answers);
            String analysis = objectMapper.createObjectNode()
                    .put("status", "BASIC_RESULT_READY")
                    .toString();
            Instant now = Instant.now();
            TestResult result = new TestResult(
                    id,
                    answersJson,
                    "UNCLASSIFIED",
                    analysis,
                    ALGORITHM_VERSION,
                    sha256(accessToken),
                    now.plusSeconds(accessTokenTtlHours * 3600),
                    now
            );
            repository.save(result);
            return new AnalysisOutcome(id, accessToken, "UNCLASSIFIED", analysis, ALGORITHM_VERSION);
        } catch (Exception exception) {
            throw new BusinessException(ErrorCode.INVALID_REQUEST, exception);
        }
    }

    public TestResult getAuthorized(UUID id, String accessToken) {
        if (accessToken == null || accessToken.isBlank()) {
            throw new BusinessException(ErrorCode.UNAUTHORIZED);
        }
        TestResult result = repository.findByIdAndAccessTokenHash(id, sha256(accessToken))
                .orElseThrow(() -> new BusinessException(ErrorCode.RESULT_ACCESS_DENIED));
        if (result.getAccessTokenExpiresAt().isBefore(Instant.now())) {
            throw new BusinessException(ErrorCode.UNAUTHORIZED);
        }
        return result;
    }

    private void validateAnswers(JsonNode answers) {
        if (answers == null
                || !answers.isArray()
                || answers.size() != REQUIRED_QUESTION_IDS.size()) {
            throw new BusinessException(ErrorCode.INVALID_REQUEST);
        }
        List<String> ids = new ArrayList<>();
        for (JsonNode answer : answers) {
            boolean hasRequiredFields = answer.isObject()
                    && !answer.path("questionId").asText().isBlank()
                    && !answer.path("choice").asText().isBlank();
            if (!hasRequiredFields) {
                throw new BusinessException(ErrorCode.INVALID_REQUEST);
            }
            ids.add(answer.path("questionId").asText());
        }
        boolean hasAllQuestions = ids.containsAll(REQUIRED_QUESTION_IDS);
        boolean hasDuplicate = ids.stream().distinct().count() != ids.size();
        if (!hasAllQuestions || hasDuplicate) {
            throw new BusinessException(ErrorCode.INVALID_REQUEST);
        }
    }

    private String randomToken() {
        byte[] bytes = new byte[32];
        secureRandom.nextBytes(bytes);
        return HexFormat.of().formatHex(bytes);
    }

    static String sha256(String value) {
        try {
            byte[] digest = MessageDigest.getInstance("SHA-256")
                    .digest(value.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(digest);
        } catch (Exception exception) {
            throw new IllegalStateException(exception);
        }
    }

}
