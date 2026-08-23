from fastapi import APIRouter, Depends, Request, status
from app.core.response import create_response
from app.db.database import get_db
from app.dependencies.auth_middleware import get_current_user
from app.services.user_service import get_user_profile_service
from sqlalchemy.orm import Session

# Nhóm endpoint liên quan đến tài khoản người dùng.
routers = APIRouter(tags=["users"])

# Lấy hồ sơ của người dùng từ token hiện tại và cơ sở dữ liệu.
@routers.get("/users/me", status_code=status.HTTP_200_OK)
def get_my_profile(request: Request, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_response(
        request,
        status.HTTP_200_OK,
        "Success",
        data=get_user_profile_service(current_user, db),
    )