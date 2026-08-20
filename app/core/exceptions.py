from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

def create_error_response(status_code: int, message: str, error, path: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "status_code": status_code,
            "message": message,
            "data": None,
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "path": path
        }
    )

def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 200:
        message = "OK"
    elif exc.status_code == 201:
        message = "Created"
    elif exc.status_code == 400:
        message = "Bad request"
    elif exc.status_code == 403:
        message = "Forbidden"
    elif exc.status_code == 404:
        message = "Resource not found"
    else:
        message = "Request failed"

    return create_error_response(
        status_code=exc.status_code,
        message=message,
        error=exc.detail,
        path=request.url.path
    )