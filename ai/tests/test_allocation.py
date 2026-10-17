import pytest

from app.config.allocation_policy import (
    AllocationPolicy,
    AllocationStrategy,
    AssetAllocation,
)
from app.schemas.allocation import (
    AllocationRecommendationRequest,
    CapacityConstraintInput,
)
from app.schemas.preference_classification import PreferenceDimensions
from app.services.allocation import recommend_allocation


def test_policy() -> AllocationPolicy:
    return AllocationPolicy(
        version="allocation-test-v1",
        strategies=(
            AllocationStrategy(
                "growth",
                "성장 시나리오",
                "HIGH",
                "LOW",
                (AssetAllocation("market-assets", 100),),
                ("장기 계획과 변동성을 확인합니다.",),
            ),
            AllocationStrategy(
                "balanced",
                "균형 시나리오",
                "MEDIUM",
                "HIGH",
                (AssetAllocation("cash", 50), AssetAllocation("bonds", 50)),
                ("목표 기간에 맞춰 유동성을 우선합니다.",),
            ),
            AllocationStrategy(
                "liquid",
                "유동성 우선 시나리오",
                "LOW",
                "HIGH",
                (AssetAllocation("cash", 100),),
                ("단기 목표의 현금 필요성을 우선합니다.",),
            ),
        ),
    )


def request_with_capacity(
    *,
    risk_ceiling: str = "MEDIUM",
    goal_horizon: str = "THREE_TO_SEVEN_YEARS",
    liquidity_assessment: str = "CONSTRAINED",
    constraint_flags: list[str] | None = None,
    missing_data: list[str] | None = None,
) -> AllocationRecommendationRequest:
    return AllocationRecommendationRequest(
        preference_scores=PreferenceDimensions(
            risk=90,
            accumulation=80,
            planning=70,
            investment=95,
        ),
        mbfi_type_id="active-investor",
        capacity=CapacityConstraintInput(
            capacity_status="CONSTRAINED_WITH_MISSING_DATA",
            constraint_flags=constraint_flags or [],
            risk_ceiling=risk_ceiling,
            liquidity_assessment=liquidity_assessment,
            goal_horizon=goal_horizon,
            missing_data=missing_data or [],
        ),
    )


def test_risk_ceiling_rejects_strategy_above_capacity() -> None:
    result = recommend_allocation(
        request_with_capacity(risk_ceiling="LOW"),
        policy=test_policy(),
    )

    assert result.selected_strategy == "liquid"
    assert "growth:CAPACITY_RISK_CEILING" in result.rejected_strategies
    assert "balanced:CAPACITY_RISK_CEILING" in result.rejected_strategies


def test_selected_allocation_totals_one_hundred_percent() -> None:
    result = recommend_allocation(request_with_capacity(), policy=test_policy())

    assert result.recommendation_status == "RECOMMENDED"
    assert result.allocation_scenario is not None
    assert result.allocation_scenario.total_percentage == 100
    assert sum(
        item.percentage for item in result.allocation_scenario.allocations
    ) == 100


def test_short_goal_rejects_low_liquidity_strategy() -> None:
    result = recommend_allocation(
        request_with_capacity(
            risk_ceiling="HIGH",
            goal_horizon="WITHIN_1_YEAR",
            liquidity_assessment="CONSTRAINED",
        ),
        policy=test_policy(),
    )

    assert result.selected_strategy == "balanced"
    assert "growth:SHORT_GOAL_LIQUIDITY" in result.rejected_strategies


def test_high_debt_rejects_non_low_risk_strategy() -> None:
    result = recommend_allocation(
        request_with_capacity(
            risk_ceiling="HIGH",
            constraint_flags=["DEBT_BURDEN_CONSTRAINT"],
        ),
        policy=test_policy(),
    )

    assert result.selected_strategy == "liquid"
    assert "growth:HIGH_DEBT_CONSTRAINT" in result.rejected_strategies
    assert "balanced:HIGH_DEBT_CONSTRAINT" in result.rejected_strategies


def test_missing_data_does_not_generate_arbitrary_allocation() -> None:
    result = recommend_allocation(
        request_with_capacity(
            risk_ceiling="UNDETERMINED",
            liquidity_assessment="INSUFFICIENT_DATA",
            missing_data=["EMERGENCY_FUND_MONTHS"],
        ),
        policy=test_policy(),
    )

    assert result.recommendation_status == "INSUFFICIENT_DATA"
    assert result.selected_strategy is None
    assert result.allocation_scenario is None


def test_unloaded_external_policy_does_not_generate_ratios() -> None:
    result = recommend_allocation(request_with_capacity(), policy=None)

    assert result.recommendation_status == "POLICY_UNAVAILABLE"
    assert result.policy_version == "allocation-policy-unavailable"
    assert result.allocation_scenario is None


def test_invalid_policy_total_is_rejected() -> None:
    invalid_policy = AllocationPolicy(
        version="allocation-invalid-v1",
        strategies=(
            AllocationStrategy(
                "invalid",
                "잘못된 시나리오",
                "LOW",
                "HIGH",
                (AssetAllocation("cash", 70),),
                (),
            ),
        ),
    )

    result = recommend_allocation(
        request_with_capacity(risk_ceiling="LOW"),
        policy=invalid_policy,
    )

    assert result.recommendation_status == "POLICY_INVALID"
    assert result.allocation_scenario is None
