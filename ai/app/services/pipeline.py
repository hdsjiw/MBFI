from app.schemas.allocation import (
    AllocationRecommendationRequest,
    CapacityConstraintInput,
)
from app.schemas.capacity import CapacityRequest
from app.schemas.pipeline import (
    AnalysisPipelineRequest,
    AnalysisPipelineResponse,
    AnalysisPolicyVersions,
)
from app.schemas.preference_classification import (
    PreferenceClassificationRequest,
    PreferenceDimensions,
)
from app.schemas.preference_scoring import PreferenceScoringRequest
from app.schemas.preference_scoring import PreferenceScoringResponse
from app.schemas.report import (
    PersonalizedReportRequest,
    ReportPreferenceInput,
)
from app.services.allocation import recommend_allocation
from app.services.capacity import evaluate_capacity
from app.services.preference_classification import classify_preference
from app.services.preference_scoring import calculate_preference_scores
from app.services.report import generate_personalized_report

PIPELINE_VERSION = "analysis-pipeline-v1"


def run_analysis_pipeline(
    request: AnalysisPipelineRequest,
) -> AnalysisPipelineResponse:
    preference_scoring = calculate_preference_scores(
        PreferenceScoringRequest(
            questionnaire_version=request.questionnaire_version,
            answers=request.preference_answers,
        )
    )
    preference_dimensions = _preference_dimensions(preference_scoring)
    classification = classify_preference(
        PreferenceClassificationRequest(dimensions=preference_dimensions)
    )
    capacity = evaluate_capacity(
        CapacityRequest(
            questionnaire_version=request.questionnaire_version,
            answers=request.financial_status_answers,
        )
    )
    capacity_input = CapacityConstraintInput.model_validate(capacity.model_dump())
    allocation = recommend_allocation(
        AllocationRecommendationRequest(
            preference_scores=preference_dimensions,
            mbfi_type_id=classification.primary.type_id,
            capacity=capacity_input,
        )
    )
    report = generate_personalized_report(
        PersonalizedReportRequest(
            preference_scoring=ReportPreferenceInput(
                scoring_version=preference_scoring.scoring_version,
                dimensions=preference_scoring.dimensions,
            ),
            mbfi_type=classification,
            capacity=capacity_input,
            allocation=allocation,
        )
    )
    policy_versions = AnalysisPolicyVersions(
        pipeline_version=PIPELINE_VERSION,
        scoring_version=preference_scoring.scoring_version,
        prototype_config_version=classification.prototype_config_version,
        capacity_policy_version=capacity.policy_version,
        allocation_policy_version=allocation.policy_version,
        report_policy_version=report.policy_versions.report_policy_version,
    )
    status = (
        "COMPLETED"
        if report.report_status == "READY"
        else "COMPLETED_WITH_LIMITATIONS"
    )
    return AnalysisPipelineResponse(
        pipeline_version=PIPELINE_VERSION,
        questionnaire_version=request.questionnaire_version,
        status=status,
        policy_versions=policy_versions,
        preference_scoring=preference_scoring,
        classification=classification,
        capacity=capacity,
        allocation=allocation,
        report=report,
    )


def _preference_dimensions(
    response: PreferenceScoringResponse,
) -> PreferenceDimensions:
    return PreferenceDimensions(
        risk=response.dimensions["Risk"].normalized_score,
        accumulation=response.dimensions["Accumulation"].normalized_score,
        planning=response.dimensions["Planning"].normalized_score,
        investment=response.dimensions["Investment"].normalized_score,
    )
