from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.response import create_response
from app.schemas.response import ResponseModel
from app.dependencies.auth_middleware import get_current_user
from typing import Optional
from app.schemas.project import (
    ProjectCreate, ProjectUpdate,
    ProjectMemberCreate, ProjectMemberUpdate
)
from app.services.project_service import(
    create_project_service,
    search_project_service,
)

routers = APIRouter(tags=["project"])

@routers.post("/projects", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
def create_project(request: Request, project: ProjectCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    new_project = create_project_service(project, current_user, db)
    return create_response(
        request,
        status.HTTP_201_CREATED,
        "Created project success",
        data={
            "id": new_project.id,
            "name": new_project.name,
            "description": new_project.description,
            "owner_id": new_project.owner_id,
            "created_at": new_project.created_at
        }
    )
    
@routers.get("/project", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def search_project(request: Request, search: Optional[str] = None, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    projects = search_project_service(db, search)
    return create_response(
        request,
        status.HTTP_200_OK,
        "Success",
        data=[
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "owner_id": project.owner_id,
                "created_at": project.created_at,
            }
            for project in projects
        ]
    )