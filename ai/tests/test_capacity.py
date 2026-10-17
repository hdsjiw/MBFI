import pytest
from pydantic import ValidationError

from app.config.capacity_policy import CAPACITY_POLICY_VERSION
from app.schemas.capacity import CapacityRequest
from app.schemas.preference_scoring import PreferenceScoringRequest
from app.services.capacity import InvalidCapacityAnswers, evaluate_capacity
from app.services.preference_scoring import calculate_preference_scores


def financial_answer(question_id: str, option: str) -> dict[str, str]:
    return {"question_id": question_id, "option_id": f"{question_id}-{option}"}


def capacity_request_with(options: dict[str, str]) -> CapacityRequest:
    answers = [
        financial_answer(f"F{index:02d}", options.get(f"F{index:02d}", "D"))
        for index in range(1, 9)
    ]
    return CapacityRequest(questionnaire_version="2026-01", answers=answers)


def test_constrained_capacity_sets_low_ceiling_and_missing_data() -> None:
    request = capacity_request_with({"F05": "A", "F06": "A", "F08": "A"})

    result = evaluate_capacity(request)

    assert result.capacity_status == "CONSTRAINED_WITH_MISSING_DATA"
    assert result.risk_ceiling == "LOW"
    assert result.liquidity_assessment == "CONSTRAINED"
    assert "LOW_SAVING_CAPACITY" in result.constraint_flags
    assert "DEBT_BURDEN_CONSTRAINT" in result.constraint_flags
    assert "SHORT_GOAL_HORIZON" in result.constraint_flags
    assert result.missing_data == [
        "INCOME_STABILITY",
        "EMERGENCY_FUND_MONTHS",
        "MAJOR_EXPENSE_WITHIN_3_YEARS",
    ]
    assert len(result.evidence) == 8
    assert result.policy_version == CAPACITY_POLICY_VERSION


def test_unrestricted_signals_do_not_claim_high_capacity() -> None:
    result = evaluate_capacity(capacity_request_with({}))

    assert result.capacity_status == "INFORMATION_INSUFFICIENT"
    assert result.constraint_flags == []
    assert result.risk_ceiling == "UNDETERMINED"
    assert result.liquidity_assessment == "INSUFFICIENT_DATA"


def test_f03_and_f04_are_not_used_to_calculate_saving_rate() -> None:
    lower_categories = capacity_request_with({"F03": "A", "F04": "D"})
    higher_categories = capacity_request_with({"F03": "D", "F04": "A"})

    lower_result = evaluate_capacity(lower_categories)
    higher_result = evaluate_capacity(higher_categories)

    assert lower_result.risk_ceiling == higher_result.risk_ceiling
    assert lower_result.constraint_flags == higher_result.constraint_flags
    assert not any("SAVING_RATE" in flag for flag in lower_result.constraint_flags)


def test_high_preference_with_low_capacity_remains_constrained() -> None:
    preference_answers = [
        {"question_id": f"Q{index:02d}", "option_id": f"Q{index:02d}-D"}
        for index in range(1, 13)
    ]
    preference_answers[2]["option_id"] = "Q03-A"
    preference = calculate_preference_scores(
        PreferenceScoringRequest(
            questionnaire_version="2026-01",
            answers=preference_answers,
        )
    )
    capacity = evaluate_capacity(
        capacity_request_with({"F05": "A", "F06": "A", "F08": "A"})
    )

    assert preference.dimensions["Risk"].normalized_score == 100
    assert preference.dimensions["Investment"].normalized_score == 100
    assert capacity.risk_ceiling == "LOW"
    assert capacity.capacity_status == "CONSTRAINED_WITH_MISSING_DATA"


def test_missing_duplicate_and_mismatched_answers_are_rejected() -> None:
    with pytest.raises(ValidationError):
        CapacityRequest(
            questionnaire_version="2026-01",
            answers=capacity_request_with({}).answers[:-1],
        )

    duplicate = capacity_request_with({})
    duplicate.answers[-1] = duplicate.answers[0]
    with pytest.raises(InvalidCapacityAnswers):
        evaluate_capacity(duplicate)

    invalid = capacity_request_with({})
    invalid.answers[0].option_id = "F02-A"
    with pytest.raises(InvalidCapacityAnswers):
        evaluate_capacity(invalid)


def test_capacity_http_endpoint_returns_policy_output() -> None:
    from fastapi.testclient import TestClient

    from app.main import app

    response = TestClient(app).post(
        "/internal/v1/capacity-constraints",
        json=capacity_request_with({"F05": "A"}).model_dump(),
    )

    assert response.status_code == 200
    assert response.json()["policy_version"] == CAPACITY_POLICY_VERSION
    assert response.json()["risk_ceiling"] == "LOW"
