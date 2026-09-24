import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.task import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    """Schema tao moi Task tu Client.
    category_id co the de trong neu task khong thuoc danh muc nao.
    """
    category_id: uuid.UUID | None = None
    title: str = Field(min_length=1, max_length=200)
    notes: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    deadline: datetime | None = None


class TaskUpdate(BaseModel):
    """Schema cap nhat thong tin Task (Partial Update).
    Cac truong deu la tuon chon (Optional), chi gui nhung truong can cap nhat.
    """
    category_id: uuid.UUID | None = None
    title: str | None = Field(default=None, min_length=1, max_length=200)
    notes: str | None = None
    is_completed: bool | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    deadline: datetime | None = None
    completed_at: datetime | None = None


class TaskRead(BaseModel):
    """Schema phan hoi thong tin Task ve cho Client.
    category_id co the la None neu cong viec khong thuoc danh muc nao.
    """
    id: uuid.UUID
    user_id: uuid.UUID
    category_id: uuid.UUID | None = None  # Co thể bằng None nếu Task không thuộc danh mục
    title: str
    notes: str | None = None
    is_completed: bool = Field(default=False)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority
    deadline: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
