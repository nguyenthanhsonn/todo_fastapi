from typing import Any
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base application exception."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "BAD_REQUEST"

    def __init__(
        self,
        message: str,
        code: str | None = None,
        status_code: int | None = None,
        fields: dict[str, str] | None = None,
    ) -> None:
        self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code
        self.fields = fields
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, resource_name: str, resource_id: Any) -> None:
        super().__init__(
            message=f"{resource_name} with id '{resource_id}' was not found.",
            code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class ValidationError(AppError):
    def __init__(self, message: str, fields: dict[str, str] | None = None) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            fields=fields,
        )


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Authentication credentials were not provided or are invalid.") -> None:
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


CredentialError = UnauthorizedError


class ForbiddenError(AppError):
    def __init__(self, message: str = "You do not have permission to perform this action.") -> None:
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class DuplicateError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            code="DUPLICATE_ERROR",
            status_code=status.HTTP_409_CONFLICT,
        )


def format_pydantic_errors(errors: list[dict[str, Any]]) -> tuple[str, dict[str, str]]:
    """Format Pydantic RequestValidationError list into clean message and fields dictionary."""
    fields: dict[str, str] = {}
    first_msg = "Validation Error"

    for err in errors:
        loc = err.get("loc", ())
        # Extract the last field name from tuple (e.g. ('body', 'title') -> 'title')
        field_name = str(loc[-1]) if loc else "non_field_error"
        msg = err.get("msg", "Invalid value")
        
        # Clean up default Pydantic message 'Field required' to 'Required'
        if msg.lower() in ["field required", "value is required"]:
            clean_msg = "Required"
        else:
            clean_msg = msg

        fields[field_name] = clean_msg

        if first_msg == "Validation Error":
            if clean_msg == "Required":
                first_msg = f"Task {field_name} is required" if field_name == "title" else f"{field_name.replace('_', ' ').capitalize()} is required"
            else:
                first_msg = clean_msg

    return first_msg, fields


def register_exception_handlers(app: FastAPI) -> None:
    """Register application-wide exception handlers with standardized error format."""

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        error_body: dict[str, Any] = {
            "code": exc.code,
            "message": exc.message,
        }
        if exc.fields:
            error_body["fields"] = exc.fields

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": error_body,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        message, fields = format_pydantic_errors(exc.errors())
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": message,
                    "fields": fields,
                },
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        code_map = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            409: "CONFLICT",
            422: "UNPROCESSABLE_ENTITY",
        }
        code_str = code_map.get(exc.status_code, "HTTP_ERROR")

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": code_str,
                    "message": str(exc.detail),
                },
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred on the server.",
                },
            },
        )
