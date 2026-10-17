package com.mbfi.payment.controller;

import com.mbfi.global.response.ApiResponse;
import com.mbfi.payment.dto.CancelPaymentRequest;
import com.mbfi.payment.dto.ConfirmPaymentRequest;
import com.mbfi.payment.dto.CreatePaymentRequest;
import com.mbfi.payment.dto.PaymentResponse;
import com.mbfi.payment.entity.Payment;
import com.mbfi.payment.service.PaymentService;
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
@RequestMapping("/api/payments")
public class PaymentController {
    private final PaymentService payments;

    public PaymentController(PaymentService payments) {
        this.payments = payments;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ApiResponse<PaymentResponse> create(@RequestBody CreatePaymentRequest request,
            @RequestHeader("X-Access-Token") String token,
            @RequestHeader("Idempotency-Key") String idempotencyKey) {
        Payment payment = payments.create(request.testResultId(), token, idempotencyKey);
        return ApiResponse.success(PaymentResponse.from(payment));
    }

    @PostMapping("/confirm")
    public ApiResponse<PaymentResponse> confirm(@RequestBody ConfirmPaymentRequest request) {
        Payment payment = payments.confirm(request.orderId(), request.paymentKey(), request.amount());
        return ApiResponse.success(PaymentResponse.from(payment));
    }

    @GetMapping("/{orderId}")
    public ApiResponse<PaymentResponse> get(
            @PathVariable String orderId,
            @RequestHeader("X-Access-Token") String token
    ) {
        Payment payment = payments.authorizedFind(orderId, token);
        return ApiResponse.success(PaymentResponse.from(payment));
    }

    @PostMapping("/{orderId}/reconcile")
    public ApiResponse<PaymentResponse> reconcile(
            @PathVariable String orderId,
            @RequestHeader("X-Access-Token") String token
    ) {
        Payment payment = payments.authorizedReconcile(orderId, token);
        return ApiResponse.success(PaymentResponse.from(payment));
    }

    @PostMapping("/{orderId}/cancel")
    public ApiResponse<PaymentResponse> cancel(@PathVariable String orderId, @RequestBody CancelPaymentRequest request,
            @RequestHeader("X-Access-Token") String token,
            @RequestHeader("Idempotency-Key") String idempotencyKey) {
        Payment payment = payments.cancel(orderId, token, idempotencyKey, request.reason());
        return ApiResponse.success(PaymentResponse.from(payment));
    }

}
