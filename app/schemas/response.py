from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str = Field(description="Error code string, e.g. VALIDATION_ERROR, NOT_FOUND")
    message: str = Field(description="Human-readable error message")
    fields: dict[str, str] | None = Field(default=None, description="Field-level validation error details")


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None
    meta: dict[str, Any] | None = Field(default=None)


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail


def success_response(data: Any = None, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    """Helper function to build a standardized success response payload.
    Omits 'meta' field if meta is None or empty.
    """
    res: dict[str, Any] = {
        "success": True,
        "data": data if data is not None else {},
    }
    if meta:
        res["meta"] = meta
    return res


def error_response(
    code: str,
    message: str,
    fields: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Helper function to build a standardized error response payload."""
    error_dict: dict[str, Any] = {
        "code": code,
        "message": message,
    }
    if fields is not None:
        error_dict["fields"] = fields
    return {
        "success": False,
        "error": error_dict,
    }
