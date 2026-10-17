from dataclasses import dataclass
from typing import Mapping

CAPACITY_POLICY_VERSION = "capacity-v0-provisional"


@dataclass(frozen=True)
class CapacityPolicy:
    f05_risk_ceiling: Mapping[str, str]
    f06_risk_ceiling: Mapping[str, str]
    f08_risk_ceiling: Mapping[str, str]
    missing_data: tuple[str, ...]


# Thresholds and policy consequences are provisional until validated with
# financial-domain stakeholders and outcome data.
CAPACITY_POLICY = CapacityPolicy(
    f05_risk_ceiling={"A": "LOW", "B": "MEDIUM"},
    f06_risk_ceiling={"A": "LOW", "B": "LOW", "C": "MEDIUM"},
    f08_risk_ceiling={"A": "LOW", "B": "MEDIUM"},
    missing_data=(
        "INCOME_STABILITY",
        "EMERGENCY_FUND_MONTHS",
        "MAJOR_EXPENSE_WITHIN_3_YEARS",
    ),
)

RISK_CEILING_ORDER = {"LOW": 0, "MEDIUM": 1, "UNDETERMINED": 2}
