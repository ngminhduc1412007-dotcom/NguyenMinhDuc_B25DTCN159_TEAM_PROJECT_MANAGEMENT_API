from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.schemas.response import ResponseModel
from app.core.response import create_response

def response_json(response: ResponseModel):
    return JSONResponse(
        status_code=response.status_code,
        content=jsonable_encoder(response.model_dump()),
    )


def http_exception_handler(request: Request, exc: HTTPException):
    response = create_response(
        request,
        exc.status_code,
        "Failed",
        errors=exc.detail,
    )
    return response_json(response)


def validation_exception_handler(request: Request, exc: RequestValidationError):
    response = create_response(
        request,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Failed",
        errors=exc.errors(),
    )
    return response_json(response)


def generic_exception_handler(request: Request, exc: Exception):
    response = create_response(
        request,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Failed",
        errors=str(exc),
    )
    return response_json(response)


def register_exception_handlers(app):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)