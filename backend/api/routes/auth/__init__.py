from fastapi import APIRouter

from backend.api.routes.auth.login import router as login_router


router = APIRouter()

router.include_router(login_router)