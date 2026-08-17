from fastapi import APIRouter, Depends

from backend.api.dependencies import get_current_admin
from backend.api.schemas.auth import UserResponse


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    username: str = Depends(get_current_admin),
) -> UserResponse:
    return UserResponse(
        username=username,
    )