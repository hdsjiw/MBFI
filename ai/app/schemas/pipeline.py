from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.capacity import CapacityResponse, FinancialStatusAnswer
from app.schemas.preference_classification import PreferenceClassification
from app.schemas.preference_scoring import (
    PreferenceScoringResponse,
    QuestionnaireAnswer,
)
from app.schemas.allocation import AllocationRecommendationResponse
from app.schemas.report import PersonalizedReportResponse


class AnalysisPipelineRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    questionnaire_version: str = Field(min_length=1, max_length=50)
    preference_answers: list[QuestionnaireAnswer] = Field(min_length=12, max_length=12)
    financial_status_answers: list[FinancialStatusAnswer] = Field(
        min_length=8,
        max_length=8,
    )


class AnalysisPolicyVersions(BaseModel):
    pipeline_version: str
    scoring_version: str
    prototype_config_version: str
    capacity_policy_version: str
    allocation_policy_version: str
    report_policy_version: str


class AnalysisPipelineResponse(BaseModel):
    pipeline_version: str
    questionnaire_version: str
    status: Literal["COMPLETED", "COMPLETED_WITH_LIMITATIONS"]
    policy_versions: AnalysisPolicyVersions
    preference_scoring: PreferenceScoringResponse
    classification: PreferenceClassification
    capacity: CapacityResponse
    allocation: AllocationRecommendationResponse
    report: PersonalizedReportResponse
