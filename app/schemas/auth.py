from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"
    
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str   