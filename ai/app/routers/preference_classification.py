from fastapi import APIRouter

from app.schemas.preference_classification import (
    PreferenceClassificationRequest,
    PreferenceClassificationResponse,
)
from app.services.preference_classification import classify_preference

router = APIRouter(prefix="/internal/v1", tags=["internal-analysis"])


@router.post(
    "/preference-classification",
    response_model=PreferenceClassificationResponse,
)
def preference_classification(
    request: PreferenceClassificationRequest,
) -> PreferenceClassificationResponse:
    return classify_preference(request)
