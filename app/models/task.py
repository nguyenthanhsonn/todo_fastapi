import uuid
from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel

from app.models.base import utc_now


class TaskPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(SQLModel, table=True):
    """Task database entity."""

    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, description="ID of the user")
    category_id: uuid.UUID | None = Field(default=None, foreign_key="categories.id", nullable=True, index=True, description="ID of the category")
    title: str = Field(min_length=1, max_length=200, description="Title of the task")
    notes: str | None = Field(default=None, description="Notes of the task")
    is_completed: bool = Field(default=False, description="Status of the task")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Priority of the task")
    deadline: datetime | None = Field(default=None, description="Deadline of the task")
    completed_at: datetime | None = Field(default=None, description="Completed at of the task")
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
