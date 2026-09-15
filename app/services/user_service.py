from uuid import UUID
from sqlmodel import Session

from app.core.exceptions import CredentialError, DuplicateError, NotFoundError
from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user import check_mail, get_user_by_email, get_user_by_id
from app.schemas.user import LoginRequest, LoginResponse, ProfileRead, RegisterRequest, UserRead


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def register_user(self, req: RegisterRequest) -> User:
        """Register a new user after verifying email uniqueness."""
        if check_mail(self.session, req.email):
            raise DuplicateError("Email already exists")

        hashed = hash_password(req.password)
        new_user = User(
            name=req.name,
            email=req.email,
            password_hash=hashed,
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def login_user(self, req: LoginRequest) -> LoginResponse:
        """Authenticate user credentials and return login response with JWT token."""
        user = get_user_by_email(self.session, req.email)
        if not user or not verify_password(req.password, user.password_hash):
            raise CredentialError("Invalid email or password")

        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
        user_read = UserRead.model_validate(user)
        return LoginResponse(user=user_read, accessToken=access_token)

    def profile_user(self, user_id: UUID) -> ProfileRead:
        """Get user profile by user ID."""
        user = get_user_by_id(self.session, user_id)
        if not user:
            raise NotFoundError(resource_name="User", resource_id=user_id)
        user_read = UserRead.model_validate(user)
        return ProfileRead(user=user_read)

    