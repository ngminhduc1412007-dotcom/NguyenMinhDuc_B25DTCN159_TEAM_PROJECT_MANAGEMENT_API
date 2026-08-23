from pydantic import BaseModel, EmailStr
from typing import Optional

# Dữ liệu cần thiết khi đăng ký tài khoản mới.
class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"

# Dữ liệu xác thực khi đăng nhập.
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str   