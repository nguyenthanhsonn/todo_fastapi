from app.services.category_service import CategoryService
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError
from sqlmodel import Session

from app.core.exceptions import UnauthorizedError
from app.core.jwt import decode_access_token
from app.database import get_session
from app.models.user import User
from app.repositories.user import get_user_by_id
from app.services.task_service import TaskService
from app.services.user_service import UserService

security = HTTPBearer()
SessionDep = Annotated[Session, Depends(get_session)]


def get_task_service(session: SessionDep) -> TaskService:
    return TaskService(session)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_current_user(
    session: SessionDep,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> User:
    """Validate JWT token from Authorization header and return current authenticated User."""
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id_str: str | None = payload.get("sub")
        if not user_id_str:
            raise UnauthorizedError("Could not validate credentials")
        user_id = UUID(user_id_str)
    except (PyJWTError, ValueError):
        raise UnauthorizedError("Invalid or expired authentication token")

    user = get_user_by_id(session, user_id)
    if not user:
        raise UnauthorizedError("User associated with token not found")

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]

# Category dependencies 
def get_category_service(
    session: SessionDep,
) -> CategoryService:
    return CategoryService(session)


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]