from fastapi import APIRouter, HTTPException

from app.schemas.capacity import CapacityRequest, CapacityResponse
from app.services.capacity import InvalidCapacityAnswers, evaluate_capacity

router = APIRouter(prefix="/internal/v1", tags=["internal-analysis"])


@router.post("/capacity-constraints", response_model=CapacityResponse)
def capacity_constraints(request: CapacityRequest) -> CapacityResponse:
    try:
        return evaluate_capacity(request)
    except InvalidCapacityAnswers as exception:
        raise HTTPException(status_code=422, detail=str(exception)) from exception
