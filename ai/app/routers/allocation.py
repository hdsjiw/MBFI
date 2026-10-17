from fastapi import APIRouter

from app.schemas.allocation import (
    AllocationRecommendationRequest,
    AllocationRecommendationResponse,
)
from app.services.allocation import recommend_allocation

router = APIRouter(prefix="/internal/v1", tags=["internal-analysis"])


@router.post(
    "/allocation-recommendation",
    response_model=AllocationRecommendationResponse,
)
def allocation_recommendation(
    request: AllocationRecommendationRequest,
) -> AllocationRecommendationResponse:
    return recommend_allocation(request)
