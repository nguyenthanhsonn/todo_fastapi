import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    """Schema tao moi Danh muc cong viec (Category)."""
    name: str = Field(min_length=1, max_length=200)
    color: str | None = Field(default=None, max_length=50)
    icon: str | None = Field(default=None, max_length=100)


class CategoryUpdate(BaseModel):
    """Schema cap nhat Danh muc (Partial Update)."""
    name: str | None = Field(default=None, min_length=1, max_length=200)
    color: str | None = Field(default=None, max_length=50)
    icon: str | None = Field(default=None, max_length=100)


class CategoryRead(BaseModel):
    """Schema phan hoi thong tin Danh muc."""
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    color: str | None = None
    icon: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
