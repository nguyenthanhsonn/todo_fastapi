from typing import Annotated, Any
from uuid import UUID
from fastapi import APIRouter, Path, Query, status

from app.dependencies import CurrentUserDep, TaskServiceDep
from app.schemas.response import ErrorResponse, SuccessResponse, success_response
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

# Khoi tao APIRouter cho Task Controller voi prefix /tasks
router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=SuccessResponse[TaskRead],
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or expired token"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
def create_task(
    req: TaskCreate,
    current_user: CurrentUserDep,
    task_service: TaskServiceDep,
) -> Any:
    """Tao cong viec moi cho nguoi dung dang dang nhap."""
    task_read = task_service.create_task(user=current_user, data=req)
    return success_response(data=task_read)


@router.get(
    "",
    response_model=SuccessResponse[list[TaskRead]],
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or expired token"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
def list_task(
    current_user: CurrentUserDep,
    task_service: TaskServiceDep,
    page: int = Query(default=1, ge=1, description="Trang hien tai (>=1)"),
    limit: int = Query(default=10, ge=1, le=100, description="So item tren 1 trang (1-100)"),
) -> Any:
    """Lay danh sach cac task cua nguoi dung kem thong tin phan trang meta."""
    tasks, meta = task_service.get_list_task(user=current_user, page=page, limit=limit)
    return success_response(data=tasks, meta=meta)


@router.get(
    "/{task_id}",  # Dung cu phap /{task_id} thay vi Express-style /:id
    response_model=SuccessResponse[TaskRead],
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or expired token"},
        404: {"model": ErrorResponse, "description": "Task not found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
def get_task_by_id(
    task_id: UUID = Path(..., description="ID cua task can lay"),
    current_user: CurrentUserDep = None,
    task_service: TaskServiceDep = None,
) -> Any:
    """Lay thong tin task theo ID."""
    task = task_service.task_id(user=current_user, task_id=task_id)
    return success_response(data=task)


@router.patch(
    "/{task_id}",
    response_model=SuccessResponse[TaskRead],
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or expired token"},
        404: {"model": ErrorResponse, "description": "Task not found"},
        422: {"model": ErrorResponse, "description": "Validation Error"},
    },
)
def update_task(
    req: TaskUpdate,
    task_id: UUID = Path(..., description="ID cua task can cap nhat"),
    current_user: CurrentUserDep = None,
    task_service: TaskServiceDep = None,
) -> Any:
    """Cap nhat thong tin task theo ID."""
    task = task_service.task_update(user=current_user, task_id=task_id, data=req)
    return success_response(data=task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid or expired token"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    },
)
def delete_task(
    task_id: UUID = Path(..., description="ID cua task can xoa"),
    current_user: CurrentUserDep = None,
    task_service: TaskServiceDep = None,
) -> None:
    """Xoa task theo ID."""
    task_service.task_delete(user=current_user, task_id=task_id)
    return None