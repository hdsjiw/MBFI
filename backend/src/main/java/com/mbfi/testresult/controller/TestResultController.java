package com.mbfi.testresult.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.mbfi.global.response.ApiResponse;
import com.mbfi.testresult.dto.AnalysisOutcome;
import com.mbfi.testresult.entity.TestResult;
import com.mbfi.testresult.service.TestAnalysisService;
import java.util.Map;
import java.util.UUID;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class TestResultController {
    private final TestAnalysisService service;

    public TestResultController(TestAnalysisService service) {
        this.service = service;
    }

    @PostMapping("/tests/analyze")
    @ResponseStatus(HttpStatus.CREATED)
    public ApiResponse<AnalysisOutcome> analyze(@RequestBody JsonNode answers) {
        AnalysisOutcome outcome = service.analyze(answers);
        return ApiResponse.success(outcome);
    }

    @GetMapping("/results/{id}")
    public ApiResponse<Map<String, Object>> result(
            @PathVariable UUID id,
            @RequestHeader(value = "X-Access-Token", required = false) String token
    ) {
        TestResult result = service.getAuthorized(id, token);
        Map<String, Object> resultData = Map.of(
                "id", result.getId(),
                "answers", result.getAnswers(),
                "financialType", result.getFinancialType(),
                "analysisResult", result.getAnalysisResult(),
                "algorithmVersion", result.getAlgorithmVersion(),
                "createdAt", result.getCreatedAt()
        );
        return ApiResponse.success(resultData);
    }
}
