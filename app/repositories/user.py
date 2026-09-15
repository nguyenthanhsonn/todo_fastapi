from sqlmodel import Session, select
from app.models.user import User
from uuid import UUID


def get_user_by_email(session: Session, email: str) -> User | None:
    """Find and return a user by email from the database."""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def get_user_by_id(session: Session, id: UUID) -> User | None:
    """Find and return a user by id from the database."""
    statement = select(User).where(User.id == id)
    return session.exec(statement).first()

def check_mail(session: Session, email: str) -> bool:
    """Check if an email already exists in the database."""
    return get_user_by_email(session, email) is not None