package com.mbfi.payment.entity;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.mbfi.global.config.JpaAuditingConfig;
import com.mbfi.payment.repository.PaymentRepository;
import java.time.Instant;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest(properties = {
        "spring.jpa.hibernate.ddl-auto=create-drop",
        "spring.sql.init.mode=never"
})
@Import(JpaAuditingConfig.class)
class PaymentAuditingTest {
    @Autowired
    private PaymentRepository paymentRepository;

    @Test
    void setsCreatedAtAndUpdatedAtOnInsertAndOnlyUpdatedAtOnChange() {
        Payment payment = new Payment(
                UUID.randomUUID(),
                UUID.randomUUID(),
                "order-audit",
                9900,
                "idempotency-audit"
        );

        Payment savedPayment = paymentRepository.saveAndFlush(payment);
        Instant createdAt = savedPayment.getCreatedAt();
        Instant updatedAt = savedPayment.getUpdatedAt();

        assertNotNull(createdAt);
        assertNotNull(updatedAt);

        savedPayment.markFailed();
        Payment changedPayment = paymentRepository.saveAndFlush(savedPayment);

        assertEquals(createdAt, changedPayment.getCreatedAt());
        assertNotNull(changedPayment.getUpdatedAt());
        assertTrue(!changedPayment.getUpdatedAt().isBefore(updatedAt));
    }
}
