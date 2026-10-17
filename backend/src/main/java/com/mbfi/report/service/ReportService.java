package com.mbfi.report.service;

import com.mbfi.global.exception.BusinessException;
import com.mbfi.global.exception.ErrorCode;
import com.mbfi.payment.entity.PaymentStatus;
import com.mbfi.payment.repository.PaymentRepository;
import com.mbfi.report.entity.Report;
import com.mbfi.report.repository.ReportRepository;
import com.mbfi.testresult.service.TestAnalysisService;
import java.time.Instant;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ReportService {
    private final TestAnalysisService results;
    private final ReportRepository reports;
    private final PaymentRepository paymentRepository;

    public ReportService(
            TestAnalysisService results,
            ReportRepository reports,
            PaymentRepository paymentRepository
    ) {
        this.results = results;
        this.reports = reports;
        this.paymentRepository = paymentRepository;
    }

    @Transactional
    public Report request(UUID resultId, String accessToken) {
        results.getAuthorized(resultId, accessToken);
        boolean paymentCompleted = paymentRepository.findByTestResultId(resultId)
                .map(payment -> payment.getStatus() == PaymentStatus.DONE)
                .orElse(false);
        if (!paymentCompleted) {
            throw new BusinessException(ErrorCode.REPORT_NOT_READY);
        }

        return reports.findByTestResultId(resultId)
                .orElseGet(() -> reports.save(new Report(UUID.randomUUID(), resultId, Instant.now())));
    }

    @Transactional(readOnly = true)
    public Report get(UUID resultId, String accessToken) {
        results.getAuthorized(resultId, accessToken);
        return reports.findByTestResultId(resultId)
                .orElseThrow(() -> new BusinessException(ErrorCode.REPORT_NOT_READY));
    }

}
