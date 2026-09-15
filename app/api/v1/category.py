from typing import Any
from uuid import UUID
from fastapi import APIRouter, status

from app.dependencies import CategoryServiceDep, CurrentUserDep
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.schemas.response import ErrorResponse, SuccessResponse, success_response

# Router khoi tao cho API Category (/categories)
router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post(
    "",
    response_model=SuccessResponse[CategoryRead],  # Dung CategoryRead thay vi TaskRead
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or expired token"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
def create_category(req: CategoryCreate, current_user: CurrentUserDep, category_service: CategoryServiceDep) -> Any:
    """Tao danh muc cho nguoi dung"""
    category_read = category_service.create_category(user=current_user, data=req)
    return success_response(data=category_read)

