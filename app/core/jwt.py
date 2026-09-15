from datetime import datetime, timedelta, timezone
import jwt
from app.config import get_settings

settings = get_settings()


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Tạo JWT access token dựa trên cấu hình SECRET_KEY, ALGORITHM từ .env."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Giải mã và xác thực JWT access token bằng cấu hình từ .env."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
