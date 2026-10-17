from app.config.report_templates import (
    DIMENSION_INTERPRETATIONS,
    DIMENSION_LABELS,
    REPORT_POLICY_VERSION,
    TYPE_REPORT_TEMPLATES,
)
from app.schemas.report import (
    AllocationChartItem,
    PersonalizedReportRequest,
    PersonalizedReportResponse,
    PolicyVersions,
    ReportChartData,
    ReportDimensionInterpretation,
    ReportPdfData,
    ReportSection,
    ScoreChartItem,
)


def generate_personalized_report(
    request: PersonalizedReportRequest,
) -> PersonalizedReportResponse:
    template = TYPE_REPORT_TEMPLATES.get(
        request.mbfi_type.primary.type_id,
        _fallback_type_template(
            request.mbfi_type.primary.type_id,
            request.mbfi_type.primary.label,
        ),
    )
    dimensions = _build_dimensions(request)
    chart_data = _build_chart_data(request, dimensions)
    capacity_explanation = _build_capacity_explanation(request)
    recommendation_explanation = _build_recommendation_explanation(request)
    behavior_guidance = _build_behavior_guidance(request, dimensions)
    methodology = _build_methodology(request)
    type_summary = ReportSection(
        title=f"{template.label} 이해하기",
        paragraphs=[template.summary, template.strengths, template.consideration],
    )
    pdf_data = ReportPdfData(
        document_title="MBFI 금융 성향 분석 리포트",
        subtitle=f"{template.label} · 교육용 분석 결과",
        sections=[
            type_summary,
            capacity_explanation,
            recommendation_explanation,
            methodology,
        ],
        charts=chart_data,
    )
    policy_versions = PolicyVersions(
        scoring_version=request.preference_scoring.scoring_version,
        prototype_config_version=request.mbfi_type.prototype_config_version,
        capacity_policy_version=request.capacity.policy_version,
        allocation_policy_version=request.allocation.policy_version,
        report_policy_version=REPORT_POLICY_VERSION,
    )
    return PersonalizedReportResponse(
        report_status=(
            "READY"
            if request.allocation.recommendation_status == "RECOMMENDED"
            else "READY_WITH_LIMITATIONS"
        ),
        title="나의 MBFI 금융 성향 리포트",
        type_summary=type_summary,
        dimensions=dimensions,
        capacity_explanation=capacity_explanation,
        recommendation_explanation=recommendation_explanation,
        behavior_guidance=behavior_guidance,
        methodology=methodology,
        chart_data=chart_data,
        pdf_data=pdf_data,
        policy_versions=policy_versions,
    )


def _build_dimensions(
    request: PersonalizedReportRequest,
) -> list[ReportDimensionInterpretation]:
    result: list[ReportDimensionInterpretation] = []
    for axis in ("Risk", "Accumulation", "Planning", "Investment"):
        dimension = request.preference_scoring.dimensions[axis]
        level = _score_level(dimension.normalized_score)
        result.append(
            ReportDimensionInterpretation(
                axis=axis,
                label=DIMENSION_LABELS[axis],
                score=dimension.normalized_score,
                interpretation_level=level,
                interpretation=DIMENSION_INTERPRETATIONS[axis][level],
            )
        )
    return result


def _build_chart_data(
    request: PersonalizedReportRequest,
    dimensions: list[ReportDimensionInterpretation],
) -> ReportChartData:
    allocation = request.allocation.allocation_scenario
    return ReportChartData(
        score_dimensions=[
            ScoreChartItem(axis=item.axis, label=item.label, score=item.score)
            for item in dimensions
        ],
        allocation=[
            AllocationChartItem(
                asset_class=item.asset_class,
                percentage=item.percentage,
            )
            for item in allocation.allocations
        ]
        if allocation
        else [],
    )


def _build_capacity_explanation(
    request: PersonalizedReportRequest,
) -> ReportSection:
    capacity = request.capacity
    paragraphs = [
        f"Capacity 상태는 {capacity.capacity_status}이며, 위험 상한은 {capacity.risk_ceiling}입니다.",
        f"목표 기간은 {capacity.goal_horizon}이고 유동성 평가는 {capacity.liquidity_assessment}입니다.",
    ]
    if capacity.constraint_flags:
        paragraphs.append(
            "적용된 제약: " + ", ".join(capacity.constraint_flags) + "."
        )
    if capacity.missing_data:
        paragraphs.append(
            "추가 확인이 필요한 정보: " + ", ".join(capacity.missing_data) + "."
        )
    return ReportSection(title="재무 제약과 목표 조건", paragraphs=paragraphs)


def _build_recommendation_explanation(
    request: PersonalizedReportRequest,
) -> ReportSection:
    allocation = request.allocation
    if allocation.allocation_scenario is None:
        return ReportSection(
            title="추천 시나리오",
            paragraphs=[
                "현재는 확정된 자산배분 정책 또는 충분한 정보가 없어 배분 비중을 제시하지 않습니다.",
                f"추천 상태: {allocation.recommendation_status}.",
                "이는 특정 금융상품이나 수익률을 추천하지 않기 위한 보류 상태입니다.",
            ],
        )
    scenario = allocation.allocation_scenario
    allocation_text = ", ".join(
        f"{item.asset_class} {item.percentage:g}%"
        for item in scenario.allocations
    )
    return ReportSection(
        title="추천 시나리오",
        paragraphs=[
            f"{scenario.label}은 교육용 자산군 시나리오이며, 특정 종목 추천이 아닙니다.",
            f"배분 예시: {allocation_text}.",
            "추천 근거: " + ", ".join(allocation.applied_constraints) + ".",
        ],
    )


def _build_behavior_guidance(
    request: PersonalizedReportRequest,
    dimensions: list[ReportDimensionInterpretation],
) -> list[str]:
    guidance = [
        "본 결과는 금융 습관을 이해하기 위한 교육용 안내이며 투자 적합성 판단이 아닙니다.",
        "목표 기간과 현금 필요성을 먼저 확인한 뒤 금융 행동의 우선순위를 정하세요.",
    ]
    if request.capacity.constraint_flags:
        guidance.append("현재 제약 조건이 해소되기 전에는 위험을 확대하는 행동을 보류하세요.")
    if any(item.axis == "Planning" and item.interpretation_level == "LOW" for item in dimensions):
        guidance.append("정기적으로 자산·지출·목표 진행 상황을 확인하는 습관부터 시작하세요.")
    if any(item.axis == "Accumulation" and item.interpretation_level == "LOW" for item in dimensions):
        guidance.append("소비 후 남은 금액이 아니라 먼저 정한 금액을 분리하는 방법을 검토하세요.")
    if any(item.axis == "Investment" and item.interpretation_level == "HIGH" for item in dimensions):
        guidance.append("시장투자 선호와 실제 Capacity를 구분하고, 정책과 목표 조건을 함께 확인하세요.")
    return guidance


def _build_methodology(request: PersonalizedReportRequest) -> ReportSection:
    return ReportSection(
        title="방법론과 유의사항",
        paragraphs=[
            "Preference 점수는 Risk, Accumulation, Planning, Investment 네 축의 입력 결과를 그대로 표시합니다.",
            "MBFI 유형과 Capacity 결과는 입력된 분석 결과를 설명에 사용하며 이 리포트에서 재계산하지 않습니다.",
            "Allocation은 외부 정책이 제공한 경우에만 자산군 비율을 표시하며, 특정 종목·예상 수익률·보장 수익을 생성하지 않습니다.",
            "프로토타입·Capacity·Allocation 정책 버전은 결과와 함께 기록되며, 현재 확정되지 않은 정책은 제한사항으로 표시해야 합니다.",
            f"리포트 템플릿 정책 버전: {REPORT_POLICY_VERSION}.",
        ],
    )


def _score_level(score: float) -> str:
    if score < 33.333333:
        return "LOW"
    if score < 66.666667:
        return "MEDIUM"
    return "HIGH"


def _fallback_type_template(type_id: str, label: str):
    from app.config.report_templates import TypeReportTemplate

    return TypeReportTemplate(
        type_id=type_id,
        label=label,
        summary="분류된 유형의 설명 템플릿이 아직 등록되지 않았습니다.",
        strengths="현재 입력된 유형 결과를 기준으로 추가 설명이 필요합니다.",
        consideration="유형만으로 투자 결정을 내리지 말고 Capacity와 목표 조건을 함께 확인하세요.",
    )
