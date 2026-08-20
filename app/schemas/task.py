from datetime import datetime
from pydantic import BaseModel

class TaskCreate(BaseModel):
    project_id: int
    title: str
    description: str
    assignee_id: int
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: datetime

class TaskUpdate(BaseModel):
    title: str 
    description: str 
    assignee_id: int 
    status: str 
    priority: str
    due_date: datetime 


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