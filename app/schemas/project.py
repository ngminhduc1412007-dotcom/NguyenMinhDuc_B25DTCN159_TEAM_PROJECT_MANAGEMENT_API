from datetime import datetime
from pydantic import BaseModel, Field

# Dữ liệu tạo project mới.
class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str

# Dữ liệu cập nhật project.
class ProjectUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str

# Dữ liệu project dùng trong response.
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int
    created_at: datetime

# Dữ liệu thêm user vào project.
class ProjectMemberCreate(BaseModel):
    user_id: int = Field(gt=0)
    role: str = "member"

# Dữ liệu đổi role của thành viên project.
class ProjectMemberUpdate(BaseModel):
    role: str

# Dữ liệu thành viên project dùng trong response.
class ProjectMemberResponse(BaseModel):
    project_id: int
    user_id: int
    role: str
    joined_at: datetime