from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from app.db.database import engine, Base
from app.core.response import create_response
from app.dependencies.auth_middleware import get_current_admin
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.routers.auth import routers as auth_router
from app.routers.admin import routers as admin_router
from app.routers.users import routers as user_router
from app.routers.projects import routers as project_router
from app.schemas.response import ResponseModel
from app.models import project, task, user

# Khởi tạo ứng dụng FastAPI trung tâm.
app = FastAPI()

# Tạo các bảng từ những model đã được import nếu chúng chưa tồn tại.
Base.metadata.create_all(bind=engine)

# Đăng ký trực tiếp từng bộ xử lý lỗi cho toàn bộ ứng dụng.
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Endpoint đơn giản để kiểm tra server đang hoạt động.
@app.get("/health-check", response_model=ResponseModel, status_code=status.HTTP_200_OK)
def checking_server(request: Request, current_user=Depends(get_current_admin)):
    return create_response(
        request,
        status.HTTP_200_OK,
        "Server is running",
    )

# Đăng ký các nhóm route của từng tính năng vào ứng dụng.
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(project_router)