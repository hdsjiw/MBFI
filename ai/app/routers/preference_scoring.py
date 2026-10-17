from fastapi import APIRouter, HTTPException

from app.schemas.preference_scoring import (
    PreferenceScoringRequest,
    PreferenceScoringResponse,
)
from app.services.preference_scoring import (
    InvalidPreferenceAnswers,
    calculate_preference_scores,
)

router = APIRouter(prefix="/internal/v1", tags=["internal-analysis"])


@router.post(
    "/preference-score",
    response_model=PreferenceScoringResponse,
)
def preference_score(
    request: PreferenceScoringRequest,
) -> PreferenceScoringResponse:
    try:
        return calculate_preference_scores(request)
    except InvalidPreferenceAnswers as exception:
        raise HTTPException(status_code=422, detail=str(exception)) from exception
