from typing import Any, Optional
from pydantic import BaseModel

class ResponseModel(BaseModel):
    status_code: int
    message: str
    data: Optional[Any] = None
    errors: Optional[Any] = None
    timestamp: str
    path: str