from fastapi import FastAPI

app = FastAPI(title="MBFI AI Server", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "UP", "service": "ai"}


@app.get("/internal/v1/report-preview")
def report_preview() -> dict[str, str]:
    """Integration placeholder. Financial interpretation is intentionally not implemented yet."""
    return {"status": "NOT_IMPLEMENTED", "message": "AI report generation will be added in a future milestone."}
