from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Dữ liệu tạo task, gồm project, người được giao và thời hạn.
class TaskCreate(BaseModel):
    title: str
    description: str
    assignee_id: int
    status: str = "todo"
    priority: str = "medium"
    due_date: Optional[datetime] = None

# Dữ liệu cập nhật đầy đủ thông tin task.
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None

# Dữ liệu task dùng để trả về cho client.
class TaskResponse(BaseModel):
    id : int
    project_id: int
    title: str
    description: str
    assignee_id: int
    status: str
    priority: str
    due_date: datetime
    created_at: datetime