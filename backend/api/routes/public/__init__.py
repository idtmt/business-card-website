from fastapi import APIRouter

from backend.api.routes.public.company import router as company_router
from backend.api.routes.public.contacts import router as contacts_router
from backend.api.routes.public.faq import router as faq_router
from backend.api.routes.public.locations import router as locations_router
from backend.api.routes.public.services import router as services_router


router = APIRouter()

router.include_router(company_router)
router.include_router(services_router)
router.include_router(contacts_router)
router.include_router(faq_router)
router.include_router(locations_router)