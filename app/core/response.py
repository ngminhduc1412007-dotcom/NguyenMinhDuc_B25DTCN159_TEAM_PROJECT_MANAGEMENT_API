from datetime import datetime
from typing import Any
from fastapi import Request
from app.schemas.response import ResponseModel

# Tạo response thống nhất, đồng thời gắn thời gian và đường dẫn request.
def create_response(request: Request, status_code: int, message: str, data: Any = None, errors: Any = None,):
    return ResponseModel(
        status_code=status_code,
        message=message,
        data=data,
        errors=errors,
        timestamp=datetime.now().isoformat(),
        path=request.url.path,
    )
