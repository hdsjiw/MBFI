package com.mbfi.payment.repository;

import com.mbfi.payment.entity.CancelStatus;
import com.mbfi.payment.entity.PaymentCancel;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PaymentCancelRepository extends JpaRepository<PaymentCancel, UUID> {
    Optional<PaymentCancel> findByIdempotencyKey(String idempotencyKey);
    boolean existsByPaymentIdAndStatus(UUID paymentId, CancelStatus status);
}
