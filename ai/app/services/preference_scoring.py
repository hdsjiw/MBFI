from dataclasses import dataclass
from typing import Mapping, Sequence

from app.schemas.preference_scoring import (
    DimensionScore,
    QuestionnaireAnswer,
    PreferenceScoringRequest,
    PreferenceScoringResponse,
    QuestionContribution,
)
from app.schemas.preference_classification import (
    PreferenceClassificationRequest,
    PreferenceDimensions,
)
from app.services.preference_classification import classify_preference

SCORING_VERSION = "preference-v1"
AXIS_QUESTION_IDS: Mapping[str, tuple[str, ...]] = {
    "Risk": ("Q01", "Q02", "Q03"),
    "Accumulation": ("Q04", "Q05", "Q06"),
    "Planning": ("Q07", "Q08", "Q09"),
    "Investment": ("Q10", "Q11", "Q12"),
}
QUESTION_SCORE_MAP: Mapping[str, Mapping[str, int]] = {
    question_id: {
        f"{question_id}-A": 1,
        f"{question_id}-B": 2,
        f"{question_id}-C": 3,
        f"{question_id}-D": 4,
    }
    for question_id in (
        "Q01", "Q02", "Q04", "Q05", "Q06",
        "Q07", "Q08", "Q09", "Q10", "Q11", "Q12",
    )
}
QUESTION_SCORE_MAP = {
    **QUESTION_SCORE_MAP,
    "Q03": {
        "Q03-A": 4,
        "Q03-B": 3,
        "Q03-C": 2,
        "Q03-D": 1,
    },
}


class InvalidPreferenceAnswers(ValueError):
    pass


@dataclass(frozen=True)
class ScoredAnswer:
    question_id: str
    option_id: str
    axis: str
    score: int


def normalize_score(raw_score: int) -> float:
    if raw_score < 3 or raw_score > 12:
        raise ValueError("raw score must be between 3 and 12")
    return ((raw_score - 3) / 9) * 100


def calculate_preference_scores(
    request: PreferenceScoringRequest,
) -> PreferenceScoringResponse:
    scored_answers = _score_answers(request.answers)
    dimensions: dict[str, DimensionScore] = {}

    for axis, question_ids in AXIS_QUESTION_IDS.items():
        raw_score = sum(
            answer.score
            for answer in scored_answers
            if answer.question_id in question_ids
        )
        dimensions[axis] = DimensionScore(
            raw_score=raw_score,
            normalized_score=normalize_score(raw_score),
        )

    contributions = [
        QuestionContribution(
            question_id=answer.question_id,
            option_id=answer.option_id,
            axis=answer.axis,
            score=answer.score,
        )
        for answer in scored_answers
    ]
    return PreferenceScoringResponse(
        scoring_version=SCORING_VERSION,
        questionnaire_version=request.questionnaire_version,
        dimensions=dimensions,
        contributions=contributions,
        classification=classify_preference(
            PreferenceClassificationRequest(
                dimensions=PreferenceDimensions(
                    risk=dimensions["Risk"].normalized_score,
                    accumulation=dimensions["Accumulation"].normalized_score,
                    planning=dimensions["Planning"].normalized_score,
                    investment=dimensions["Investment"].normalized_score,
                )
            )
        ),
    )


def _score_answers(answers: Sequence[QuestionnaireAnswer]) -> list[ScoredAnswer]:
    expected_ids = {
        question_id
        for question_ids in AXIS_QUESTION_IDS.values()
        for question_id in question_ids
    }
    received_ids = [answer.question_id for answer in answers]
    if len(received_ids) != len(set(received_ids)):
        raise InvalidPreferenceAnswers("duplicate question responses are not allowed")
    if set(received_ids) != expected_ids:
        raise InvalidPreferenceAnswers("all Q01-Q12 responses are required")

    axis_by_question = {
        question_id: axis
        for axis, question_ids in AXIS_QUESTION_IDS.items()
        for question_id in question_ids
    }
    scored_answers: list[ScoredAnswer] = []
    for answer in answers:
        score = QUESTION_SCORE_MAP.get(answer.question_id, {}).get(answer.option_id)
        if score is None:
            raise InvalidPreferenceAnswers(
                f"invalid option {answer.option_id} for {answer.question_id}"
            )
        scored_answers.append(
            ScoredAnswer(
                question_id=answer.question_id,
                option_id=answer.option_id,
                axis=axis_by_question[answer.question_id],
                score=score,
            )
        )
    return scored_answers
