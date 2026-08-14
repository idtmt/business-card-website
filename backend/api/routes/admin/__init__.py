from fastapi import APIRouter, Depends

from backend.api.dependencies import get_current_admin

from backend.api.routes.admin.company import router as company_router
from backend.api.routes.admin.contacts import router as contacts_router
from backend.api.routes.admin.faq import router as faq_router
from backend.api.routes.admin.locations import router as locations_router
from backend.api.routes.admin.prices import router as prices_router
from backend.api.routes.admin.schedules import router as schedules_router
from backend.api.routes.admin.services import router as services_router


router = APIRouter(
    prefix="/admin",
    dependencies=[
        Depends(get_current_admin),
    ],
)

router.include_router(company_router)
router.include_router(services_router)
router.include_router(contacts_router)
router.include_router(faq_router)
router.include_router(prices_router)
router.include_router(schedules_router)
router.include_router(locations_router)