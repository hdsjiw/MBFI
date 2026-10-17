from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.preference_classification import PreferenceClassification

class QuestionnaireAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: str = Field(pattern=r"^Q(0[1-9]|1[0-2])$")
    option_id: Literal[
        "Q01-A", "Q01-B", "Q01-C", "Q01-D",
        "Q02-A", "Q02-B", "Q02-C", "Q02-D",
        "Q03-A", "Q03-B", "Q03-C", "Q03-D",
        "Q04-A", "Q04-B", "Q04-C", "Q04-D",
        "Q05-A", "Q05-B", "Q05-C", "Q05-D",
        "Q06-A", "Q06-B", "Q06-C", "Q06-D",
        "Q07-A", "Q07-B", "Q07-C", "Q07-D",
        "Q08-A", "Q08-B", "Q08-C", "Q08-D",
        "Q09-A", "Q09-B", "Q09-C", "Q09-D",
        "Q10-A", "Q10-B", "Q10-C", "Q10-D",
        "Q11-A", "Q11-B", "Q11-C", "Q11-D",
        "Q12-A", "Q12-B", "Q12-C", "Q12-D",
    ]


class PreferenceScoringRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    questionnaire_version: str = Field(min_length=1, max_length=50)
    answers: list[QuestionnaireAnswer] = Field(min_length=12, max_length=12)


class DimensionScore(BaseModel):
    raw_score: int = Field(ge=3, le=12)
    normalized_score: float = Field(ge=0, le=100)


class QuestionContribution(BaseModel):
    question_id: str
    option_id: str
    axis: str
    score: int = Field(ge=1, le=4)


class PreferenceScoringResponse(BaseModel):
    scoring_version: str
    questionnaire_version: str
    dimensions: dict[str, DimensionScore]
    contributions: list[QuestionContribution]
    classification: PreferenceClassification
