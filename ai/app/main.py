from fastapi import FastAPI

from app.routers.preference_scoring import router as preference_scoring_router
from app.routers.preference_classification import (
    router as preference_classification_router,
)
from app.routers.capacity import router as capacity_router
from app.routers.allocation import router as allocation_router
from app.routers.report import router as report_router
from app.routers.pipeline import router as pipeline_router

app = FastAPI(title="MBFI AI Server", version="0.1.0")
app.include_router(preference_scoring_router)
app.include_router(preference_classification_router)
app.include_router(capacity_router)
app.include_router(allocation_router)
app.include_router(report_router)
app.include_router(pipeline_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "UP", "service": "ai"}


@app.get("/internal/v1/report-preview")
def report_preview() -> dict[str, str]:
    """Integration placeholder. Financial interpretation is intentionally not implemented yet."""
    return {"status": "NOT_IMPLEMENTED", "message": "AI report generation will be added in a future milestone."}
