from datetime import datetime
from typing import Any
from pydantic import BaseModel

class ResponseModel(BaseModel):
    status_code: int
    message: str
    data: Any = None
    error: Any = None
    timestamp: datetime
    path: str