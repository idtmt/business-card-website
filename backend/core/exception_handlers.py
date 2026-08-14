from fastapi import Request
from fastapi.responses import JSONResponse

from backend.core.exceptions import (
    NotFoundError,
    ValidationError,
)


async def validation_error_handler(
    request: Request,
    exc: ValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": str(exc),
        },
    )


async def not_found_error_handler(
    request: Request,
    exc: NotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
        },
    )


from fastapi import Request
from fastapi.responses import JSONResponse

from backend.core.exceptions import AlreadyExistsError


async def already_exists_error_handler(
    request: Request,
    exc: AlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc),
        },
    )