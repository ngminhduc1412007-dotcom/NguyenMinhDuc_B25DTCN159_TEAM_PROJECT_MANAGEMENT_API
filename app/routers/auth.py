from fastapi import APIRouter, Depends, Request, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest
)
from app.schemas.response import ResponseModel
from app.core.response import create_response
from app.services.auth_service import(
    register_service,
    login_service
)

# Nhóm endpoint đăng ký và đăng nhập.
routers = APIRouter(tags=["authentication"])

# Tạo tài khoản rồi trả về các thông tin an toàn của người dùng.
@routers.post("/auth/register", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
def register(request: Request, user: UserRegisterRequest, db: Session = Depends(get_db)):
    created_user = register_service(user, db)
    return create_response(
        request,
        status.HTTP_201_CREATED,
        "Created",
        data={
            "id": created_user.id,
            "email": created_user.email,
            "full_name": created_user.full_name,
            "role": created_user.role,
            "is_active": created_user.is_active,
            "created_at": created_user.created_at,
        },
    )

# Xác thực thông tin đăng nhập và trả về access token.
@routers.post("/auth/login", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def login(request: Request, user: UserLoginRequest, db: Session = Depends(get_db)):
    login_data = login_service(user, db)
    return create_response(request, status.HTTP_200_OK, "Success", data=login_data)