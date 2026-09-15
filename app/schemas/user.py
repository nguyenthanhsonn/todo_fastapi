import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# Schema cho Request Đăng ký tài khoản từ Client
class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200, description="Tên người dùng")
    email: EmailStr = Field(description="Email người dùng")
    password: str = Field(min_length=6, max_length=100, description="Mật khẩu (tối thiểu 6 ký tự)")

    @field_validator("email")
    @classmethod
    def validate_gmail_address(cls, v: str) -> str:
        """Kiểm tra và bắt buộc email phải có định dạng đuôi @gmail.com hợp lệ."""
        clean_email = v.strip().lower()
        if not clean_email.endswith("@gmail.com"):
            raise ValueError("Email phải đúng định dạng @gmail.com")
        return clean_email

# Schema cho thông tin User trả về bên trong key "data" của SuccessResponse
class UserRead(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    created_at: datetime

    # Cho phép Pydantic đọc dữ liệu trực tiếp từ SQLModel ORM Object
    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: EmailStr = Field(description="Email người dùng")
    password: str = Field(min_length=1, description="Mật khẩu người dùng")
    @field_validator("email")
    @classmethod
    def validate_gmail_address(cls, v: str) -> str:
        """Kiểm tra và bắt buộc email phải có định dạng đuôi @gmail.com hợp lệ."""
        clean_email = v.strip().lower()
        if not clean_email.endswith("@gmail.com"):
            raise ValueError("Email phải đúng định dạng @gmail.com")
        return clean_email

class LoginResponse(BaseModel):
    user: UserRead
    accessToken: str

class ProfileRead(BaseModel):
    user: UserRead
