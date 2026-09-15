from uuid import UUID
from sqlmodel import Session, select

from app.core.exceptions import NotFoundError
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate


class CategoryService:
    """Service layer xu ly logic nghiep vu cho Category (Danh muc cong viec)."""

    def __init__(self, session: Session):
        self.session = session

    def create_category(self, user: User, data: CategoryCreate) -> CategoryRead:
        """Tao danh muc moi cho nguoi dung."""
        category = Category(
            user_id=user.id,
            name=data.name,
            color=data.color,
            icon=data.icon,
        )
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return CategoryRead.model_validate(category)