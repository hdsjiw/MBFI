package com.mbfi.testresult.repository;

import com.mbfi.testresult.entity.TestResult;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TestResultRepository extends JpaRepository<TestResult, UUID> {
    Optional<TestResult> findByIdAndAccessTokenHash(UUID id, String accessTokenHash);
}
