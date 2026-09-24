import uuid
from typing import Any
from uuid import UUID
from sqlmodel import Session, func, select

from app.core.exceptions import NotFoundError
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate


class TaskService:
    """Service layer xu ly logic nghiep vu cho Task.
    
    Luu y: Nhan doi tuong `user: User` tu API Controller truyen sang,
    KHONG import `CurrentUserDep` tu dependencies de tranh loi Circular Import.
    """

    def __init__(self, session: Session):
        self.session = session

    def create_task(self, user: User, data: TaskCreate) -> TaskRead:
        """Tao task moi cho nguoi dung."""
        is_completed = True if data.status == TaskStatus.DONE else False
        task = Task(
            user_id=user.id,
            category_id=data.category_id,
            title=data.title,
            notes=data.notes,
            status=data.status,
            is_completed=is_completed,
            priority=data.priority,
            deadline=data.deadline,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return TaskRead.model_validate(task)

    def get_list_task(
        self, user: User, page: int = 1, limit: int = 10
    ) -> tuple[list[TaskRead], dict[str, Any]]:
        """Lay danh sach cac task cua nguoi dung va thong tin phan trang meta.
        
        Args:
            user: User can xac thuc.
            page: Trang can lay (bat dau tu 1).
            limit: So luong item/trang (default 10).

        Returns:
            tuple[list[TaskRead], dict[str, Any]]: (danh sach task, dict metadata)
        """
        page = max(1, page)
        limit = max(1, limit)
        offset = (page - 1) * limit

        # 1. Tinh tong so luong task (total) cua nguoi dung trong CSDL
        total_stmt = select(func.count()).select_from(Task).where(Task.user_id == user.id)
        total = self.session.exec(total_stmt).one()

        # 2. Tinh so luong task da hoan thanh (completed)
        completed_stmt = (
            select(func.count())
            .select_from(Task)
            .where(Task.user_id == user.id, Task.is_completed == True)
        )
        completed = self.session.exec(completed_stmt).one()

        # 3. So luong task chua hoan thanh (active)
        active = total - completed

        # 4. Lay danh sach task thuoc trang hien tai
        statement = select(Task).where(Task.user_id == user.id).offset(offset).limit(limit)
        tasks = self.session.exec(statement).all()

        meta = {
            "total": total,
            "active": active,
            "completed": completed,
            "page": page,
            "limit": limit,
        }

        return [TaskRead.model_validate(t) for t in tasks], meta

    def _get_task_entity(self, user: User, task_id: UUID) -> Task:
        """Helper noi bo: Lay ORM Task entity theo ID va Kiem tra quyen so huu cua user."""
        statement = select(Task).where(Task.user_id == user.id, Task.id == task_id)
        task = self.session.exec(statement).first()
        if not task:
            raise NotFoundError(resource_name="Task", resource_id=task_id)
        return task

    def task_id(self, user: User, task_id: UUID) -> TaskRead:
        """Lay thong tin task theo ID."""
        task = self._get_task_entity(user, task_id)
        return TaskRead.model_validate(task)
    
    def task_update(self, user: User, task_id: UUID, data: TaskUpdate) -> TaskRead:
        """Cap nhat thong tin task theo ID (Partial Update)."""
        task = self._get_task_entity(user, task_id)
        update_data = data.model_dump(exclude_unset=True)

        if "status" in update_data and "is_completed" not in update_data:
            if update_data["status"] == TaskStatus.DONE:
                update_data["is_completed"] = True
            elif task.is_completed:
                update_data["is_completed"] = False
        elif "is_completed" in update_data and "status" not in update_data:
            if update_data["is_completed"]:
                update_data["status"] = TaskStatus.DONE
            elif task.status == TaskStatus.DONE:
                update_data["status"] = TaskStatus.TODO

        for key, value in update_data.items():
            setattr(task, key, value)
            
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return TaskRead.model_validate(task)
    
    def task_delete(self, user: User, task_id: UUID) -> None:
        """Xoa task theo ID."""
        task = self._get_task_entity(user, task_id)
        self.session.delete(task)
        self.session.commit()