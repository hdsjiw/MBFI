from dataclasses import dataclass

from app.config.allocation_policy import (
    ALLOCATION_POLICY,
    AllocationPolicy,
    AllocationStrategy,
)
from app.schemas.allocation import (
    AllocationItem,
    AllocationRecommendationRequest,
    AllocationRecommendationResponse,
    AllocationScenario,
    RecommendationEvidence,
)

RISK_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
POLICY_UNAVAILABLE_VERSION = "allocation-policy-unavailable"


@dataclass(frozen=True)
class StrategyDecision:
    strategy: AllocationStrategy
    rejection_reason: str | None


def recommend_allocation(
    request: AllocationRecommendationRequest,
    policy: AllocationPolicy | None = ALLOCATION_POLICY,
) -> AllocationRecommendationResponse:
    evidence = [
        RecommendationEvidence(
            source="preference_scores",
            detail="Preference scores are provided as context; MBFI type alone does not determine allocation.",
        ),
        RecommendationEvidence(
            source="mbfi_type",
            detail=f"Received type_id={request.mbfi_type_id}; type is not used as a standalone allocation rule.",
        ),
    ]
    applied_constraints = _applied_constraints(request)
    if _has_insufficient_capacity_data(request):
        return _without_allocation(
            status="INSUFFICIENT_DATA",
            policy_version=_policy_version(policy),
            applied_constraints=applied_constraints,
            evidence=evidence,
            detail="Capacity or liquidity information is insufficient for an allocation scenario.",
        )
    if policy is None:
        return _without_allocation(
            status="POLICY_UNAVAILABLE",
            policy_version=POLICY_UNAVAILABLE_VERSION,
            applied_constraints=applied_constraints,
            evidence=evidence,
            detail="No approved external allocation policy with asset-class ratios is loaded.",
        )

    invalid_strategy = next(
        (strategy for strategy in policy.strategies if not _has_valid_total(strategy)),
        None,
    )
    if invalid_strategy is not None:
        return _without_allocation(
            status="POLICY_INVALID",
            policy_version=policy.version,
            applied_constraints=applied_constraints,
            evidence=evidence,
            detail=f"Strategy {invalid_strategy.strategy_id} allocation must total 100%.",
        )

    decisions = [
        StrategyDecision(strategy, _rejection_reason(strategy, request))
        for strategy in policy.strategies
    ]
    rejected = [
        f"{decision.strategy.strategy_id}:{decision.rejection_reason}"
        for decision in decisions
        if decision.rejection_reason
    ]
    selected = next(
        (decision.strategy for decision in decisions if decision.rejection_reason is None),
        None,
    )
    if selected is None:
        return _without_allocation(
            status="NO_ELIGIBLE_STRATEGY",
            policy_version=policy.version,
            applied_constraints=applied_constraints,
            evidence=evidence,
            rejected_strategies=rejected,
            detail="Every configured strategy violates an applied constraint.",
        )

    evidence.append(
        RecommendationEvidence(
            source="policy",
            detail=f"Selected the first eligible strategy in policy order: {selected.strategy_id}.",
        )
    )
    return AllocationRecommendationResponse(
        recommendation_status="RECOMMENDED",
        selected_strategy=selected.strategy_id,
        allocation_scenario=_scenario(selected),
        applied_constraints=applied_constraints,
        rejected_strategies=rejected,
        behavior_guidance=list(selected.behavior_guidance),
        evidence=evidence,
        policy_version=policy.version,
    )


def _has_insufficient_capacity_data(
    request: AllocationRecommendationRequest,
) -> bool:
    capacity = request.capacity
    return (
        capacity.capacity_status == "INFORMATION_INSUFFICIENT"
        or capacity.risk_ceiling == "UNDETERMINED"
        or capacity.liquidity_assessment == "INSUFFICIENT_DATA"
        or bool(capacity.missing_data)
    )


def _applied_constraints(request: AllocationRecommendationRequest) -> list[str]:
    capacity = request.capacity
    constraints = [f"RISK_CEILING_{capacity.risk_ceiling}"]
    constraints.append(f"GOAL_HORIZON_{capacity.goal_horizon}")
    constraints.append(f"LIQUIDITY_{capacity.liquidity_assessment}")
    constraints.extend(capacity.constraint_flags)
    return constraints


def _rejection_reason(
    strategy: AllocationStrategy,
    request: AllocationRecommendationRequest,
) -> str | None:
    capacity = request.capacity
    if RISK_ORDER[strategy.risk_level] > RISK_ORDER[capacity.risk_ceiling]:
        return "CAPACITY_RISK_CEILING"
    if (
        capacity.goal_horizon == "WITHIN_1_YEAR"
        and strategy.liquidity_profile != "HIGH"
    ):
        return "SHORT_GOAL_LIQUIDITY"
    if (
        "DEBT_BURDEN_CONSTRAINT" in capacity.constraint_flags
        and strategy.risk_level != "LOW"
    ):
        return "HIGH_DEBT_CONSTRAINT"
    if (
        capacity.liquidity_assessment == "CONSTRAINED"
        and strategy.liquidity_profile == "LOW"
    ):
        return "LIQUIDITY_CONSTRAINT"
    return None


def _has_valid_total(strategy: AllocationStrategy) -> bool:
    return abs(sum(item.percentage for item in strategy.allocations) - 100) < 1e-9


def _scenario(strategy: AllocationStrategy) -> AllocationScenario:
    allocations = [
        AllocationItem(
            asset_class=item.asset_class,
            percentage=item.percentage,
        )
        for item in strategy.allocations
    ]
    return AllocationScenario(
        strategy_id=strategy.strategy_id,
        label=strategy.label,
        allocations=allocations,
        total_percentage=sum(item.percentage for item in allocations),
    )


def _without_allocation(
    *,
    status: str,
    policy_version: str,
    applied_constraints: list[str],
    evidence: list[RecommendationEvidence],
    detail: str,
    rejected_strategies: list[str] | None = None,
) -> AllocationRecommendationResponse:
    evidence.append(RecommendationEvidence(source="engine", detail=detail))
    return AllocationRecommendationResponse(
        recommendation_status=status,
        selected_strategy=None,
        allocation_scenario=None,
        applied_constraints=applied_constraints,
        rejected_strategies=rejected_strategies or [],
        behavior_guidance=[],
        evidence=evidence,
        policy_version=policy_version,
    )


def _policy_version(policy: AllocationPolicy | None) -> str:
    return policy.version if policy else POLICY_UNAVAILABLE_VERSION
