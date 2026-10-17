from fastapi import APIRouter

from app.schemas.report import (
    PersonalizedReportRequest,
    PersonalizedReportResponse,
)
from app.services.report import generate_personalized_report

router = APIRouter(prefix="/internal/v1", tags=["internal-report"])


@router.post("/personalized-report", response_model=PersonalizedReportResponse)
def personalized_report(
    request: PersonalizedReportRequest,
) -> PersonalizedReportResponse:
    return generate_personalized_report(request)
