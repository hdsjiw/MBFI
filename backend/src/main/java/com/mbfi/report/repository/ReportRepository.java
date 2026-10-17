package com.mbfi.report.repository;

import com.mbfi.report.entity.Report;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ReportRepository extends JpaRepository<Report, UUID> {
    Optional<Report> findByTestResultId(UUID testResultId);
}
