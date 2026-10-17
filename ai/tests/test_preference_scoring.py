import pytest
from pydantic import ValidationError

from app.schemas.preference_scoring import PreferenceScoringRequest
from app.services.preference_scoring import (
    SCORING_VERSION,
    InvalidPreferenceAnswers,
    calculate_preference_scores,
)


def answer(question_id: str, option: str) -> dict[str, str]:
    return {"question_id": question_id, "option_id": f"{question_id}-{option}"}


def request_with(options: dict[str, str]) -> PreferenceScoringRequest:
    answers = [
        answer(f"Q{index:02d}", options.get(f"Q{index:02d}", "B"))
        for index in range(1, 13)
    ]
    return PreferenceScoringRequest(questionnaire_version="2026-01", answers=answers)


def test_low_and_high_boundaries_are_zero_and_one_hundred() -> None:
    low_options = {"Q01": "A", "Q02": "A", "Q03": "D"}
    high_options = {"Q01": "D", "Q02": "D", "Q03": "A"}

    low = calculate_preference_scores(request_with(low_options))
    high = calculate_preference_scores(request_with(high_options))

    assert low.dimensions["Risk"].raw_score == 3
    assert low.dimensions["Risk"].normalized_score == 0
    assert high.dimensions["Risk"].raw_score == 12
    assert high.dimensions["Risk"].normalized_score == 100


def test_q03_is_reverse_scored_but_q06_and_q09_are_forward_scored() -> None:
    request = request_with({"Q03": "A", "Q06": "D", "Q09": "D"})

    result = calculate_preference_scores(request)

    assert result.dimensions["Risk"].raw_score == 6
    assert result.dimensions["Accumulation"].raw_score == 9
    assert result.dimensions["Planning"].raw_score == 9
    assert next(item.score for item in result.contributions if item.question_id == "Q03") == 4
    assert next(item.score for item in result.contributions if item.question_id == "Q06") == 4
    assert next(item.score for item in result.contributions if item.question_id == "Q09") == 4


def test_missing_duplicate_and_invalid_answers_are_rejected() -> None:
    with pytest.raises(ValidationError):
        PreferenceScoringRequest(
            questionnaire_version="2026-01",
            answers=request_with({}).answers[:-1],
        )

    duplicate = request_with({})
    duplicate.answers[-1] = duplicate.answers[0]
    with pytest.raises(InvalidPreferenceAnswers):
        calculate_preference_scores(duplicate)

    with pytest.raises(ValidationError):
        invalid_payload = request_with({}).model_dump()
        invalid_payload["answers"][0]["option_id"] = "Q01-Z"
        PreferenceScoringRequest.model_validate(invalid_payload)


def test_scoring_is_reproducible_and_includes_version_and_contributions() -> None:
    request = request_with({"Q01": "C", "Q07": "D", "Q12": "A"})

    first = calculate_preference_scores(request)
    second = calculate_preference_scores(request)

    assert first == second
    assert first.scoring_version == SCORING_VERSION
    assert len(first.contributions) == 12


def test_http_endpoint_returns_scores_and_validation_errors() -> None:
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    payload = request_with({"Q03": "D"}).model_dump()

    response = client.post("/internal/v1/preference-score", json=payload)
    invalid_response = client.post(
        "/internal/v1/preference-score",
        json={"questionnaire_version": "2026-01", "answers": []},
    )

    assert response.status_code == 200
    assert set(response.json()["dimensions"]) == {
        "Risk", "Accumulation", "Planning", "Investment"
    }
    assert response.json()["classification"]["classification_status"] == "PROVISIONAL"
    assert "probability" not in response.json()["classification"]
    assert invalid_response.status_code == 422
