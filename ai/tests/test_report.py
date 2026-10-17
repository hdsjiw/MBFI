from app.schemas.allocation import (
    AllocationItem,
    AllocationRecommendationResponse,
    AllocationScenario,
    CapacityConstraintInput,
)
from app.schemas.preference_classification import (
    PreferenceClassification,
    PreferenceDimensions,
    RankedPreferenceType,
)
from app.schemas.preference_scoring import DimensionScore
from app.schemas.report import PersonalizedReportRequest, ReportPreferenceInput
from app.services.report import generate_personalized_report


def classification() -> PreferenceClassification:
    return PreferenceClassification(
        prototype_config_version="prototype-v0-provisional",
        classification_status="PROVISIONAL",
        boundary=False,
        boundary_distance_gap=20,
        primary=RankedPreferenceType(
            type_id="balanced-growth",
            label="균형 성장형",
            distance=0,
        ),
        secondary=RankedPreferenceType(
            type_id="long-term-growth",
            label="장기 성장형",
            distance=20,
        ),
    )


def capacity(missing_data: list[str] | None = None) -> CapacityConstraintInput:
    return CapacityConstraintInput(
        capacity_status="CONSTRAINED_WITH_MISSING_DATA",
        constraint_flags=[],
        risk_ceiling="MEDIUM",
        liquidity_assessment="CONSTRAINED",
        goal_horizon="THREE_TO_SEVEN_YEARS",
        missing_data=missing_data or [],
        policy_version="capacity-v0-provisional",
    )


def preference() -> ReportPreferenceInput:
    return ReportPreferenceInput(
        scoring_version="preference-v1",
        dimensions={
            "Risk": DimensionScore(raw_score=8, normalized_score=55.555555),
            "Accumulation": DimensionScore(raw_score=9, normalized_score=66.666667),
            "Planning": DimensionScore(raw_score=6, normalized_score=33.333333),
            "Investment": DimensionScore(raw_score=10, normalized_score=77.777778),
        },
    )


def allocation(
    status: str = "POLICY_UNAVAILABLE",
    scenario: AllocationScenario | None = None,
) -> AllocationRecommendationResponse:
    return AllocationRecommendationResponse(
        recommendation_status=status,
        selected_strategy=scenario.strategy_id if scenario else None,
        allocation_scenario=scenario,
        applied_constraints=["RISK_CEILING_MEDIUM"],
        rejected_strategies=[],
        behavior_guidance=[],
        evidence=[],
        policy_version="allocation-policy-unavailable",
    )


def report_request(
    *,
    capacity_result: CapacityConstraintInput | None = None,
    allocation_result: AllocationRecommendationResponse | None = None,
) -> PersonalizedReportRequest:
    return PersonalizedReportRequest(
        preference_scoring=preference(),
        mbfi_type=classification(),
        capacity=capacity_result or capacity(),
        allocation=allocation_result or allocation(),
    )


def test_report_is_deterministic_and_contains_pdf_and_chart_data() -> None:
    scenario = AllocationScenario(
        strategy_id="balanced",
        label="균형 시나리오",
        allocations=[
            AllocationItem(asset_class="cash", percentage=50),
            AllocationItem(asset_class="bonds", percentage=50),
        ],
        total_percentage=100,
    )
    request = report_request(
        allocation_result=allocation("RECOMMENDED", scenario),
    )

    first = generate_personalized_report(request)
    second = generate_personalized_report(request)

    assert first == second
    assert first.report_status == "READY"
    assert len(first.dimensions) == 4
    assert [item.score for item in first.chart_data.score_dimensions] == [
        55.555555, 66.666667, 33.333333, 77.777778
    ]
    assert first.chart_data.allocation[0].asset_class == "cash"
    assert first.pdf_data.charts == first.chart_data
    assert first.policy_versions.report_policy_version == "report-v1-provisional"


def test_withheld_recommendation_still_generates_limited_report() -> None:
    request = report_request(
        capacity_result=capacity(["EMERGENCY_FUND_MONTHS"]),
        allocation_result=allocation(),
    )

    result = generate_personalized_report(request)

    assert result.report_status == "READY_WITH_LIMITATIONS"
    assert result.chart_data.allocation == []
    assert result.pdf_data.sections
    assert "충분한 정보가 없어" in result.recommendation_explanation.paragraphs[0]
    assert result.policy_versions.capacity_policy_version == "capacity-v0-provisional"


def test_unknown_type_uses_safe_fallback_template() -> None:
    request = report_request()
    request.mbfi_type.primary.type_id = "unknown-type"
    request.mbfi_type.primary.label = "알 수 없는 유형"

    result = generate_personalized_report(request)

    assert "템플릿이 아직 등록되지 않았습니다" in result.type_summary.paragraphs[0]


def test_report_does_not_create_return_predictions_or_recalculate_scores() -> None:
    result = generate_personalized_report(report_request())

    assert not any("수익률" in paragraph for paragraph in result.methodology.paragraphs)
    assert result.dimensions[0].score == 55.555555
