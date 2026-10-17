import hmac
import os

from fastapi import Header, HTTPException


def require_internal_service_token(
    token: str | None = Header(default=None, alias="X-Internal-Service-Token"),
) -> None:
    expected_token = os.getenv("MBFI_AI_INTERNAL_TOKEN", "")
    if not expected_token:
        raise HTTPException(
            status_code=503,
            detail="Internal analysis authentication is not configured.",
        )
    if not token or not hmac.compare_digest(token, expected_token):
        raise HTTPException(
            status_code=401,
            detail="Internal service authentication failed.",
        )
