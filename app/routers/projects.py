from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.response import create_response
from app.schemas.response import ResponseModel
from app.dependencies.auth_middleware import get_current_user
from typing import Optional
from app.schemas.project import (
    ProjectCreate, ProjectUpdate,
    ProjectMemberCreate
)
from app.services.project_service import(
    create_project_service,
    search_project_service,
    get_project_by_id_service,
    update_project_service,
    delete_project_service
)
from app.services.project_member_service import(
    add_project_member_service,
    remove_project_member_service,
    get_project_members_service
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
    
@routers.get("/projects", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def search_project(request: Request, search: Optional[str] = None, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    projects = search_project_service(current_user, db, search)
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
    
@routers.get("/projects/{id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def get_project_by_id(request: Request, id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    get_project = get_project_by_id_service(id, current_user, db)
    return create_response(
        request,
        status.HTTP_200_OK,
        "Success",
        data=[
            {
                "id": get_project.id,
                "name": get_project.name,
                "description": get_project.description,
                "owner_id": get_project.owner_id,
                "created_at": get_project.created_at
            }
        ]
    )
    
@routers.put("/owner/project/{id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def update_project(request: Request, id: int, update_project: ProjectUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    project = update_project_service(id, update_project, current_user, db)
    return create_response(
        request,
        status.HTTP_200_OK,
        "Success",
        data=[
            {
                "id": project.id,
                "name": project.name,
                "description": project.description
            }
        ]
    )

@routers.delete("/owner/project/{id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def delete_project(request: Request, id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    project = delete_project_service(id, current_user, db)
    return create_response(
        request,
        status.HTTP_200_OK,
        "Project deleted successfully",
        data=project
    )

@routers.post("/projects/{id}/members", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
def add_project_member(request: Request, id: int, member: ProjectMemberCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    project_member = add_project_member_service(id, member, current_user, db)
    return create_response(
        request,
        status.HTTP_201_CREATED,
        "Member added successfully",
        data={
            "project_id": project_member.project_id,
            "user_id": project_member.user_id,
            "role": project_member.role,
            "joined_at": project_member.joined_at
        }
    )

@routers.delete("/projects/{id}/members/{user_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def remove_project_member(request: Request, id: int, user_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    member = remove_project_member_service(id, user_id, current_user, db)
    return create_response(
        request,
        status.HTTP_200_OK,
        "Member removed successfully",
        data={
            "project_id": member.project_id,
            "user_id": member.user_id,
            "role": member.role,
            "joined_at": member.joined_at
        }
    )

@routers.get("/projects/{id}/members", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def list_project_members(request: Request, id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    members = get_project_members_service(id, current_user, db)
    return create_response(
        request,
        status.HTTP_200_OK,
        "Success",
        data=[
            {
                "project_id": member.project_id,
                "user_id": member.user_id,
                "role": member.role,
                "joined_at": member.joined_at
            }
            for member in members
        ]
    )