from fastapi import Cookie, Depends, HTTPException, status

from backend.core.security import decode_access_token

from backend.repositories.company_repository import CompanyRepository
from backend.repositories.contact_repository import ContactRepository
from backend.repositories.faq_repository import FaqRepository
from backend.repositories.location_repository import LocationRepository
from backend.repositories.price_repository import PriceRepository
from backend.repositories.schedule_repository import ScheduleRepository
from backend.repositories.service_repository import ServiceRepository

from backend.services.company_service import CompanyService
from backend.services.contact_service import ContactService
from backend.services.faq_service import FaqService
from backend.services.location_service import LocationService
from backend.services.price_service import PriceService
from backend.services.schedule_service import ScheduleService
from backend.services.service_service import ServiceService
from backend.services.public_location_service import PublicLocationService
from backend.services.public_service_service import PublicServiceService


def get_company_repository() -> CompanyRepository:
    return CompanyRepository()


def get_contact_repository() -> ContactRepository:
    return ContactRepository()


def get_faq_repository() -> FaqRepository:
    return FaqRepository()


def get_location_repository() -> LocationRepository:
    return LocationRepository()


def get_price_repository() -> PriceRepository:
    return PriceRepository()


def get_schedule_repository() -> ScheduleRepository:
    return ScheduleRepository()


def get_service_repository() -> ServiceRepository:
    return ServiceRepository()


def get_company_service(
    repository: CompanyRepository = Depends(
        get_company_repository,
    ),
) -> CompanyService:
    return CompanyService(
        repository=repository,
    )


def get_contact_service(
    repository: ContactRepository = Depends(
        get_contact_repository,
    ),
) -> ContactService:
    return ContactService(
        repository=repository,
    )


def get_faq_service(
    repository: FaqRepository = Depends(
        get_faq_repository,
    ),
) -> FaqService:
    return FaqService(
        repository=repository,
    )


def get_service_service(
    repository: ServiceRepository = Depends(
        get_service_repository,
    ),
) -> ServiceService:
    return ServiceService(
        repository=repository,
    )


def get_price_service(
    repository: PriceRepository = Depends(
        get_price_repository,
    ),
    service_repository: ServiceRepository = Depends(
        get_service_repository,
    ),
) -> PriceService:
    return PriceService(
        repository=repository,
        service_repository=service_repository,
    )


def get_location_service(
    repository: LocationRepository = Depends(
        get_location_repository,
    ),
) -> LocationService:
    return LocationService(
        repository=repository,
    )


def get_schedule_service(
    repository: ScheduleRepository = Depends(
        get_schedule_repository,
    ),
    location_repository: LocationRepository = Depends(
        get_location_repository,
    ),
) -> ScheduleService:
    return ScheduleService(
        repository=repository,
        location_repository=location_repository,
    )


def get_public_location_service(
    location_repository: LocationRepository = Depends(
        get_location_repository,
    ),
    schedule_repository: ScheduleRepository = Depends(
        get_schedule_repository,
    ),
) -> PublicLocationService:
    return PublicLocationService(
        location_repository=location_repository,
        schedule_repository=schedule_repository,
    )


def get_public_service_service(
    service_repository: ServiceRepository = Depends(
        get_service_repository,
    ),
    price_repository: PriceRepository = Depends(
        get_price_repository,
    ),
) -> PublicServiceService:
    return PublicServiceService(
        service_repository=service_repository,
        price_repository=price_repository,
    )


async def get_current_admin(
    access_token: str | None = Cookie(
        default=None,
    ),
) -> str:
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация.",
        )

    return decode_access_token(
        access_token,
    )