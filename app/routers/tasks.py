from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.response import create_response
from app.schemas.response import ResponseModel
from app.dependencies.auth_middleware import get_current_user
from typing import Literal, Optional
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import (
    create_task_service,
    get_tasks_service,
    get_task_by_id_service,
    update_task_service,
    delete_task_service
)

routers = APIRouter(tags=["task"])

@routers.post("/projects/{id}/tasks", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
def create_task(request: Request, id: int, task: TaskCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = create_task_service(id, task, current_user, db)
    return create_response(
        request,
        status.HTTP_201_CREATED,
        "Created task success",
        data={
            "id": new_task.id,
            "project_id": new_task.project_id,
            "title": new_task.title,
            "description": new_task.description,
            "assignee_id": new_task.assignee_id,
            "status": new_task.status,
            "priority": new_task.priority,
            "due_date": new_task.due_date,
            "created_at": new_task.created_at
        }
    )
    
@routers.get("/projects/{id}/tasks", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def get_tasks(request: Request, id: int, search: Optional[str] = None,
              #Literal[...]: Giới hạn giá trị biến chỉ được phép là chuỗi
              sort_by: Literal["created_at", "due_date"] = "created_at",
              sort_order: Literal["asc", "desc"] = "asc",
              limit: int = Query(10, ge=1, le=100),
              offset: int = Query(0, ge=0),
              current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = get_tasks_service(id, current_user, db, search, sort_by, sort_order, limit, offset)
    return create_response(
        request,
        status.HTTP_200_OK,
        "Success",
        data=[
            {
                "id": task.id,
                "project_id": task.project_id,
                "title": task.title,
                "description": task.description,
                "assignee_id": task.assignee_id,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date,
                "created_at": task.created_at
            }
            for task in tasks
        ]
    )
    
@routers.get("/tasks/{id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def get_task_by_id(request: Request, id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    task = get_task_by_id_service(id, current_user, db)
    return create_response(
        request,
        status.HTTP_200_OK,
        "Success",
        data={
            "id": task.id,
            "project_id": task.project_id,
            "title": task.title,
            "description": task.description,
            "assignee_id": task.assignee_id,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date,
            "created_at": task.created_at
        }
    )

@routers.patch("/tasks/{id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def update_task(request: Request, id: int, task_update: TaskUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    task = update_task_service(id, task_update, current_user, db)
    return create_response(
        request,
        status.HTTP_200_OK,
        "Task updated successfully",
        data={
            "id": task.id,
            "project_id": task.project_id,
            "title": task.title,
            "description": task.description,
            "assignee_id": task.assignee_id,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date,
            "created_at": task.created_at
        }
    )

@routers.delete("/tasks/{id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def delete_task(request: Request, id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted_task = delete_task_service(id, current_user, db)
    return create_response(
        request,
        status.HTTP_200_OK,
        "Task deleted successfully",
        data=deleted_task
    )