from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core.exception_handlers import (
    not_found_error_handler,
    validation_error_handler,
    already_exists_error_handler
)
from backend.core.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    ValidationError,
)

from backend.api.routes.admin import router as admin_router
from backend.api.routes.auth import router as auth_router
from backend.api.routes.public import router as public_router
from backend.config import settings
from backend.database.init_db import DatabaseInitializer


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncGenerator[None, None]:
    await DatabaseInitializer.initialize()

    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)


app.add_exception_handler(
    AlreadyExistsError,
    already_exists_error_handler,
)

app.add_exception_handler(
    ValidationError,
    validation_error_handler,
)

app.add_exception_handler(
    NotFoundError,
    not_found_error_handler,
)


app.include_router(
    public_router,
    prefix="/api",
)

app.include_router(
    auth_router,
    prefix="/api",
)

app.include_router(
    admin_router,
    prefix="/api",
)