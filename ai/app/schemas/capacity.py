from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class FinancialStatusAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_id: Literal["F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08"]
    option_id: Literal[
        "F01-A", "F01-B", "F01-C", "F01-D",
        "F02-A", "F02-B", "F02-C", "F02-D",
        "F03-A", "F03-B", "F03-C", "F03-D",
        "F04-A", "F04-B", "F04-C", "F04-D",
        "F05-A", "F05-B", "F05-C", "F05-D",
        "F06-A", "F06-B", "F06-C", "F06-D",
        "F07-A", "F07-B", "F07-C", "F07-D",
        "F08-A", "F08-B", "F08-C", "F08-D",
    ]


class CapacityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    questionnaire_version: str = Field(min_length=1, max_length=50)
    answers: list[FinancialStatusAnswer] = Field(min_length=8, max_length=8)


class CapacityEvidence(BaseModel):
    question_id: str
    option_id: str
    signal: str


class CapacityResponse(BaseModel):
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
    evidence: list[CapacityEvidence]
    policy_version: str
