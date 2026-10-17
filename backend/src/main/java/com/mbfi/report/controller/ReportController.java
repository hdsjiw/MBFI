package com.mbfi.report.controller;

import com.mbfi.global.response.ApiResponse;
import com.mbfi.report.entity.Report;
import com.mbfi.report.service.ReportService;
import java.util.Map;
import java.util.UUID;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/reports")
public class ReportController {
    private final ReportService reports;

    public ReportController(ReportService reports) {
        this.reports = reports;
    }

    @GetMapping("/{resultId}")
    public ApiResponse<Map<String, Object>> get(
            @PathVariable UUID resultId,
            @RequestHeader("X-Access-Token") String token
    ) {
        Report report = reports.request(resultId, token);
        String storageKey = report.getStorageKey();
        if (storageKey == null) {
            storageKey = "";
        }
        Map<String, Object> reportData = Map.of(
                "id", report.getId(),
                "testResultId", report.getTestResultId(),
                "status", report.getStatus().name(),
                "storageKey", storageKey
        );
        return ApiResponse.success(reportData);
    }
}
