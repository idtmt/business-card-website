from fastapi import APIRouter

from backend.api.routes.auth.login import router as login_router
from backend.api.routes.auth.me import router as me_router


router = APIRouter()

router.include_router(login_router)
router.include_router(me_router)