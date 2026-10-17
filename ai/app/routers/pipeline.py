from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.schemas.pipeline import AnalysisPipelineRequest, AnalysisPipelineResponse
from app.security.internal import require_internal_service_token
from app.services.capacity import InvalidCapacityAnswers
from app.services.pipeline import run_analysis_pipeline
from app.services.preference_scoring import InvalidPreferenceAnswers

router = APIRouter(prefix="/internal/v1", tags=["analysis-pipeline"])


@router.post(
    "/analysis-pipeline",
    response_model=AnalysisPipelineResponse,
    dependencies=[Depends(require_internal_service_token)],
)
def analysis_pipeline(
    request: AnalysisPipelineRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> AnalysisPipelineResponse:
    if idempotency_key is not None and not idempotency_key.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key must not be blank.",
        )
    try:
        return run_analysis_pipeline(request)
    except (InvalidPreferenceAnswers, InvalidCapacityAnswers) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Analysis pipeline failed.",
        ) from exc
