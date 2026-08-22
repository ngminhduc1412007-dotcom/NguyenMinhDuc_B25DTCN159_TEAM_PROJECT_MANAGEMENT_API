from typing import Optional

from fastapi import APIRouter, Depends, status, Request
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.core.response import create_response
from app.schemas.response import ResponseModel
from app.dependencies.auth_middleware import get_current_admin
from app.services.admin_service import get_all_user_service, get_user_by_id_service, list_users_service

routers = APIRouter(prefix="/admin", tags=["admin"])

@routers.get("/users", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def get_all_user(request: Request, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return create_response(
        request,
        status.HTTP_200_OK,
        "Success",
        data=get_all_user_service(db)
    )

@routers.get("/users/{user_id}", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, request: Request, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return create_response(
        request,
        status.HTTP_200_OK,
        "Success",
        data=get_user_by_id_service(user_id, db)
    )

@routers.get("/user", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def search_user(request: Request, search: Optional[str] = None, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return create_response(
        request,
        status.HTTP_200_OK,
        "Success",
        data=list_users_service(db, search)
    )