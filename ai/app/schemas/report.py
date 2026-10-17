from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.allocation import (
    AllocationRecommendationResponse,
    CapacityConstraintInput,
)
from app.schemas.preference_classification import (
    PreferenceClassification,
    PreferenceDimensions,
)
from app.schemas.preference_scoring import DimensionScore


class ReportPreferenceInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scoring_version: str
    dimensions: dict[str, DimensionScore]

    @model_validator(mode="after")
    def validate_dimensions(self) -> "ReportPreferenceInput":
        expected_axes = {"Risk", "Accumulation", "Planning", "Investment"}
        if set(self.dimensions) != expected_axes:
            raise ValueError("all four preference dimensions are required")
        return self


class ReportSection(BaseModel):
    title: str
    paragraphs: list[str]


class ReportDimensionInterpretation(BaseModel):
    axis: str
    label: str
    score: float = Field(ge=0, le=100)
    interpretation_level: Literal["LOW", "MEDIUM", "HIGH"]
    interpretation: str


class ScoreChartItem(BaseModel):
    axis: str
    label: str
    score: float = Field(ge=0, le=100)


class AllocationChartItem(BaseModel):
    asset_class: str
    percentage: float = Field(ge=0, le=100)


class ReportChartData(BaseModel):
    score_dimensions: list[ScoreChartItem]
    allocation: list[AllocationChartItem]


class ReportPdfData(BaseModel):
    document_title: str
    subtitle: str
    sections: list[ReportSection]
    charts: ReportChartData


class PolicyVersions(BaseModel):
    scoring_version: str
    prototype_config_version: str
    capacity_policy_version: str
    allocation_policy_version: str
    report_policy_version: str


class PersonalizedReportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    preference_scoring: ReportPreferenceInput
    mbfi_type: PreferenceClassification
    capacity: CapacityConstraintInput
    allocation: AllocationRecommendationResponse


class PersonalizedReportResponse(BaseModel):
    report_status: Literal["READY", "READY_WITH_LIMITATIONS"]
    title: str
    type_summary: ReportSection
    dimensions: list[ReportDimensionInterpretation]
    capacity_explanation: ReportSection
    recommendation_explanation: ReportSection
    behavior_guidance: list[str]
    methodology: ReportSection
    chart_data: ReportChartData
    pdf_data: ReportPdfData
    policy_versions: PolicyVersions
