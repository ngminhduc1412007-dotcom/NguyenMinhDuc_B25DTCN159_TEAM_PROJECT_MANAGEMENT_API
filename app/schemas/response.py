from typing import Any, Optional
from pydantic import BaseModel

# Cấu trúc phản hồi chung cho cả dữ liệu thành công và lỗi.
class ResponseModel(BaseModel):
    status_code: int
    message: str
    data: Optional[Any] = None
    errors: Optional[Any] = None
    timestamp: str
    path: str