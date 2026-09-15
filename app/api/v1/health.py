from typing import Any
from fastapi import APIRouter

from app.config import get_settings
from app.schemas.response import SuccessResponse, success_response

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=SuccessResponse[dict[str, str]])
def health_check() -> Any:
    """Return application health status in standardized success format."""
    settings = get_settings()
    data = {
        "status": "ok",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }
    return success_response(data=data)
