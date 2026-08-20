from datetime import datetime
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    description: str
    
class ProjectUpdate(BaseModel):
    name: str
    description: str
    
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int
    created_at: datetime
    
class ProjectMemberCreate(BaseModel):
    user_id: int
    role: str = "MEMBER"

class ProjectMemberUpdate(BaseModel):
    role: str

class ProjectMemberResponse(BaseModel):
    project_id: int
    user_id: int
    role: str
    joined_at: datetime