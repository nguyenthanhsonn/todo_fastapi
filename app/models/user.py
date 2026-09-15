import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.base import utc_now


class User(SQLModel, table=True):
    """Application user database entity."""

    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(min_length=1, max_length=200, description="Name of the user")
    email: str = Field(index=True, unique=True, max_length=255, description="Email of the user")
    password_hash: str = Field(min_length=1, description="Hashed password of the user")
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
