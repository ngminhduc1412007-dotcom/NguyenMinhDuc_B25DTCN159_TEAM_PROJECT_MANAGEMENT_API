from fastapi import APIRouter, Depends, status, Request
from app.db.database import get_db
from sqlalchemy.orm import Session
from typing import Optional
from app.core.response import create_response
from app.schemas.response import ResponseModel
from app.dependencies.auth_middleware import get_current_admin
from app.services.admin_service import get_users_service

# Các endpoint quản trị đều dùng prefix /admin và yêu cầu quyền admin.
routers = APIRouter(tags=["admin"])

# Lấy user theo id, tìm theo từ khóa hoặc lấy toàn bộ user.
@routers.get("/users/", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def get_users(request: Request, search: Optional[str] = None, is_active: Optional[bool] = None, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return create_response(
        request,
        status.HTTP_200_OK,
        "Success",
        data=get_users_service(db, search, is_active)
    )
    