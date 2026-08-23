from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.schemas.response import ResponseModel
from app.core.response import create_response

# Chuyển một ResponseModel thành phản hồi JSON mà FastAPI có thể trả về.
def response_json(response: ResponseModel):
    return JSONResponse(
        status_code=response.status_code,
        content=jsonable_encoder(response.model_dump()),
    )

# Chuẩn hóa lỗi HTTPException về cùng cấu trúc phản hồi của ứng dụng.
def http_exception_handler(request: Request, exc: HTTPException):
    response = create_response(
        request,
        exc.status_code,
        "Failed",
        errors=exc.detail,
    )
    return response_json(response)

# Trả về chi tiết các lỗi khi dữ liệu request không vượt qua validation.
def validation_exception_handler(request: Request, exc: RequestValidationError):
    response = create_response(
        request,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Failed",
        errors=exc.errors(),
    )
    return response_json(response)

# Bắt các lỗi ngoài dự kiến để API vẫn trả về JSON thống nhất.
def generic_exception_handler(request: Request, exc: Exception):
    response = create_response(
        request,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Failed",
        errors=str(exc),
    )
    return response_json(response)