import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.base import utc_now


class Category(SQLModel, table=True):
    """Task category database entity."""

    __tablename__ = "categories"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, description="ID of the user")
    name: str = Field(min_length=1, max_length=200, description="Name of the category")
    color: str | None = Field(default=None, max_length=50, description="Color of the category")
    icon: str | None = Field(default=None, max_length=100, description="Icon of the category")
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
