from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.preference_classification import PreferenceDimensions


class CapacityConstraintInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capacity_status: Literal[
        "CONSTRAINED_WITH_MISSING_DATA",
        "INFORMATION_INSUFFICIENT",
    ]
    constraint_flags: list[str]
    risk_ceiling: Literal["LOW", "MEDIUM", "UNDETERMINED"]
    liquidity_assessment: Literal["CONSTRAINED", "INSUFFICIENT_DATA"]
    goal_horizon: Literal[
        "WITHIN_1_YEAR",
        "ONE_TO_THREE_YEARS",
        "THREE_TO_SEVEN_YEARS",
        "AFTER_7_YEARS",
    ]
    missing_data: list[str]
    policy_version: str = "capacity-v0-provisional"


class AllocationRecommendationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    preference_scores: PreferenceDimensions
    mbfi_type_id: str = Field(min_length=1, max_length=80)
    capacity: CapacityConstraintInput


class AllocationItem(BaseModel):
    asset_class: str
    percentage: float = Field(ge=0, le=100)


class AllocationScenario(BaseModel):
    strategy_id: str
    label: str
    allocations: list[AllocationItem]
    total_percentage: float = Field(ge=0, le=100)


class RecommendationEvidence(BaseModel):
    source: str
    detail: str


class AllocationRecommendationResponse(BaseModel):
    recommendation_status: Literal[
        "RECOMMENDED",
        "INSUFFICIENT_DATA",
        "POLICY_UNAVAILABLE",
        "POLICY_INVALID",
        "NO_ELIGIBLE_STRATEGY",
    ]
    selected_strategy: str | None
    allocation_scenario: AllocationScenario | None
    applied_constraints: list[str]
    rejected_strategies: list[str]
    behavior_guidance: list[str]
    evidence: list[RecommendationEvidence]
    policy_version: str
