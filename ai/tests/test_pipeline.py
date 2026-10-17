import json

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _payload() -> dict:
    return {
        "questionnaire_version": "questionnaire-v1",
        "preference_answers": [
            {"question_id": f"Q{index:02d}", "option_id": f"Q{index:02d}-B"}
            for index in range(1, 13)
        ],
        "financial_status_answers": [
            {"question_id": f"F{index:02d}", "option_id": f"F{index:02d}-B"}
            for index in range(1, 9)
        ],
    }


@pytest.fixture(autouse=True)
def internal_token(monkeypatch):
    monkeypatch.setenv("MBFI_AI_INTERNAL_TOKEN", "pipeline-test-token")


def test_pipeline_runs_in_order_and_returns_versioned_result():
    response = client.post(
        "/internal/v1/analysis-pipeline",
        headers={"X-Internal-Service-Token": "pipeline-test-token"},
        json=_payload(),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "COMPLETED_WITH_LIMITATIONS"
    assert body["policy_versions"]["pipeline_version"] == "analysis-pipeline-v1"
    assert body["preference_scoring"]["scoring_version"] == "preference-v1"
    assert body["classification"]["primary"]["type_id"]
    assert body["capacity"]["policy_version"] == "capacity-v0-provisional"
    assert body["allocation"]["recommendation_status"] == "INSUFFICIENT_DATA"
    assert body["report"]["report_status"] == "READY_WITH_LIMITATIONS"
    assert body["report"]["chart_data"]["allocation"] == []
    assert "preference_answers" not in json.dumps(body)
    assert "financial_status_answers" not in json.dumps(body)


def test_pipeline_is_deterministic_for_same_request():
    headers = {
        "X-Internal-Service-Token": "pipeline-test-token",
        "Idempotency-Key": "analysis-request-1",
    }

    first = client.post("/internal/v1/analysis-pipeline", headers=headers, json=_payload())
    second = client.post("/internal/v1/analysis-pipeline", headers=headers, json=_payload())

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()


def test_pipeline_rejects_missing_or_invalid_internal_token(monkeypatch):
    missing = client.post("/internal/v1/analysis-pipeline", json=_payload())
    invalid = client.post(
        "/internal/v1/analysis-pipeline",
        headers={"X-Internal-Service-Token": "wrong-token"},
        json=_payload(),
    )

    monkeypatch.delenv("MBFI_AI_INTERNAL_TOKEN")
    unconfigured = client.post(
        "/internal/v1/analysis-pipeline",
        headers={"X-Internal-Service-Token": "pipeline-test-token"},
        json=_payload(),
    )

    assert missing.status_code == 401
    assert invalid.status_code == 401
    assert unconfigured.status_code == 503


def test_pipeline_rejects_incomplete_questionnaire():
    payload = _payload()
    payload["preference_answers"] = payload["preference_answers"][:-1]

    response = client.post(
        "/internal/v1/analysis-pipeline",
        headers={"X-Internal-Service-Token": "pipeline-test-token"},
        json=payload,
    )

    assert response.status_code == 422


def test_pipeline_rejects_blank_idempotency_key():
    response = client.post(
        "/internal/v1/analysis-pipeline",
        headers={
            "X-Internal-Service-Token": "pipeline-test-token",
            "Idempotency-Key": "   ",
        },
        json=_payload(),
    )

    assert response.status_code == 400


def test_existing_health_and_preview_routes_remain_available():
    health = client.get("/health")
    preview = client.get("/internal/v1/report-preview")

    assert health.status_code == 200
    assert preview.status_code == 200
