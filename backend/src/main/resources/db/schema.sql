CREATE TABLE IF NOT EXISTS test_result (
    id UUID PRIMARY KEY,
    answers TEXT NOT NULL,
    financial_type VARCHAR(100) NOT NULL,
    analysis_result TEXT NOT NULL,
    algorithm_version VARCHAR(50) NOT NULL,
    access_token_hash VARCHAR(64) NOT NULL,
    access_token_expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS payment (
    id UUID PRIMARY KEY,
    test_result_id UUID NOT NULL REFERENCES test_result(id),
    order_id VARCHAR(100) NOT NULL UNIQUE,
    payment_key VARCHAR(200) UNIQUE,
    amount BIGINT NOT NULL,
    status VARCHAR(30) NOT NULL,
    idempotency_key VARCHAR(100) NOT NULL UNIQUE,
    approved_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS payment_cancel (
    id UUID PRIMARY KEY,
    payment_id UUID NOT NULL REFERENCES payment(id),
    idempotency_key VARCHAR(100) NOT NULL UNIQUE,
    pg_transaction_key VARCHAR(200) UNIQUE,
    cancel_amount BIGINT NOT NULL,
    reason VARCHAR(500) NOT NULL,
    status VARCHAR(30) NOT NULL,
    requested_at TIMESTAMP NOT NULL,
    canceled_at TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS report (
    id UUID PRIMARY KEY,
    test_result_id UUID NOT NULL UNIQUE REFERENCES test_result(id),
    status VARCHAR(30) NOT NULL,
    storage_key VARCHAR(500) NULL,
    created_at TIMESTAMP NOT NULL,
    generated_at TIMESTAMP NULL
);
