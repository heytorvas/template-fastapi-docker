from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


def _generate_error(code: int, exc: Exception, internal: bool = False):
    status_code = code // 100
    validation_error = isinstance(exc,
                                  (RequestValidationError, ValidationError))
    error_message = 'Validation Error.' if validation_error else str(exc)

    if not error_message:
        error_message = exc.detail

    if validation_error:
        errors = exc.errors()
        return {
            "content": {
                "error": {
                    "code":
                    42200,
                    "message":
                    "Validation error.",
                    "errors": [{
                        "location":
                        ".".join([str(loc) for loc in error["loc"]]),
                        "message":
                        error["msg"],
                    } for error in errors],
                }
            },
            "status_code": 422,
        }

    return {
        "content": {
            "error": {
                "code": code,
                "message":
                "Internal Server Error." if internal else error_message,
            }
        },
        "status_code": status_code,
    }


def error_handler(app: FastAPI) -> None:
    """Error handler for application."""

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_request: Request,
                                       exc: RequestValidationError):
        return JSONResponse(**_generate_error(42200, exc))

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_request: Request, exc: HTTPException):
        return JSONResponse(**_generate_error(exc.status_code * 100, exc))

    @app.exception_handler(Exception)
    async def generic_error_handler(_request: Request, exc: Exception):
        return JSONResponse(**_generate_error(50010, exc, internal=True))
