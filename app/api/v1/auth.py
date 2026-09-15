from typing import Any
from fastapi import APIRouter, status

from app.dependencies import CurrentUserDep, UserServiceDep
from app.schemas.response import ErrorResponse, SuccessResponse, success_response
from app.schemas.user import LoginRequest, LoginResponse, RegisterRequest, UserRead

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "Email already exists"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
def register_user(
    req: RegisterRequest,
    user_service: UserServiceDep,
) -> Any:
    """Register a new user account."""
    user = user_service.register_user(req)
    user_read = UserRead.model_validate(user)
    return success_response(data=user_read)


@router.post(
    "/login",
    response_model=SuccessResponse[LoginResponse],
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid email or password"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
def login_user(
    req: LoginRequest,
    user_service: UserServiceDep,
) -> Any:
    """Login to system and return user info with JWT access token."""
    login_res = user_service.login_user(req)
    return success_response(data=login_res)


@router.post(
    "/logout",
    response_model=SuccessResponse[dict[str, str]],
    status_code=status.HTTP_200_OK,
)
def logout_user() -> Any:
    """Logout user from the system."""
    return success_response(data={"message": "Logged out successfully"})


@router.get(
    "/me",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or expired token"},
    },
)
def get_profile(
    current_user: CurrentUserDep,
) -> Any:
    """Get profile of current authenticated user via Bearer Token."""
    user_read = UserRead.model_validate(current_user)
    return success_response(data=user_read)