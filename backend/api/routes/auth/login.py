from fastapi import APIRouter, HTTPException, Response, status

from backend.api.schemas.auth import (
    LoginRequest,
    LoginResponse,
)
from backend.config import settings
from backend.core.security import (
    create_access_token,
    verify_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    data: LoginRequest,
    response: Response,
) -> LoginResponse:
    if data.username != settings.admin_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль.",
        )

    if not verify_password(
        data.password,
        settings.admin_password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль.",
        )

    token = create_access_token()

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_same_site,
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )

    return LoginResponse(
        message="Авторизация выполнена успешно.",
    )


@router.post("/logout")
async def logout(
    response: Response,
) -> dict[str, str]:
    response.delete_cookie(
        key="access_token",
        path="/",
    )

    return {
        "message": "Выход выполнен успешно.",
    }