from dataclasses import dataclass
from typing import Literal

AllocationRisk = Literal["LOW", "MEDIUM", "HIGH"]
LiquidityProfile = Literal["HIGH", "MEDIUM", "LOW"]


@dataclass(frozen=True)
class AssetAllocation:
    asset_class: str
    percentage: float


@dataclass(frozen=True)
class AllocationStrategy:
    strategy_id: str
    label: str
    risk_level: AllocationRisk
    liquidity_profile: LiquidityProfile
    allocations: tuple[AssetAllocation, ...]
    behavior_guidance: tuple[str, ...]


@dataclass(frozen=True)
class AllocationPolicy:
    version: str
    strategies: tuple[AllocationStrategy, ...]


# No production allocation ratios are defined until the external policy is
# approved. Tests inject a policy object to validate engine constraints.
ALLOCATION_POLICY: AllocationPolicy | None = None
