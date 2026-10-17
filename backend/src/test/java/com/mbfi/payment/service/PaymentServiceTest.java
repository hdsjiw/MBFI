package com.mbfi.payment.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.mbfi.global.exception.BusinessException;
import com.mbfi.payment.client.FakePaymentGatewayClient;
import com.mbfi.payment.entity.Payment;
import com.mbfi.testresult.service.TestAnalysisService;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class PaymentServiceTest {
    @Test
    void successfulApprovalCallsGatewayOnce() {
        var results = mock(TestAnalysisService.class);
        var states = mock(PaymentStateService.class);
        var gateway = new FakePaymentGatewayClient();
        var payment = new Payment(UUID.randomUUID(), UUID.randomUUID(), "order-1", 9900, "idem-1");
        when(states.find("order-1")).thenReturn(payment);
        when(states.beginConfirm("order-1", "pk-1", 9900)).thenReturn(payment);
        when(states.finishConfirm(eq("order-1"), eq("pk-1"), any())).thenReturn(payment);
        var service = new PaymentService(results, states, gateway, 9900);

        service.confirm("order-1", "pk-1", 9900);

        assertEquals(1, gateway.confirmCalls);
        verify(states).finishConfirm(eq("order-1"), eq("pk-1"), any());
    }

    @Test
    void timeoutMarksPaymentUnknown() {
        var states = mock(PaymentStateService.class);
        var gateway = new FakePaymentGatewayClient();
        gateway.timeout = true;
        var payment = new Payment(UUID.randomUUID(), UUID.randomUUID(), "order-2", 9900, "idem-2");
        when(states.find("order-2")).thenReturn(payment);
        when(states.beginConfirm("order-2", "pk-2", 9900)).thenReturn(payment);
        when(states.markUnknown("order-2")).thenReturn(payment);
        var service = new PaymentService(mock(TestAnalysisService.class), states, gateway, 9900);

        assertThrows(BusinessException.class, () -> service.confirm("order-2", "pk-2", 9900));

        verify(states).markUnknown("order-2");
        verify(states, never()).markFailed("order-2");
    }
}
