from datetime import datetime 
from pydantic import BaseModel, EmailStr

# Dữ liệu đầu vào để tạo người dùng.
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = 'user'

# Các trường có thể cập nhật của người dùng.
class UserUpdate(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    is_active: bool

# Dữ liệu người dùng được phép trả về, không bao gồm password.
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

# Dữ liệu đăng nhập theo nhóm schema user.
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Token JWT trả về sau khi đăng nhập thành công.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"