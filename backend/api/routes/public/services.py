from fastapi import APIRouter, Depends

from backend.api.dependencies import get_public_service_service
from backend.api.schemas.public_service import PublicServiceResponse
from backend.services.public_service_service import PublicServiceService


router = APIRouter(
    prefix="/services",
    tags=["Public Services"],
)


@router.get(
    "",
    response_model=list[PublicServiceResponse],
)
async def get_services(
    service: PublicServiceService = Depends(
        get_public_service_service,
    ),
) -> list[PublicServiceResponse]:
    return await service.get_all()


@router.get(
    "/{service_id}",
    response_model=PublicServiceResponse,
)
async def get_service(
    service_id: int,
    service: PublicServiceService = Depends(
        get_public_service_service,
    ),
) -> PublicServiceResponse:
    return await service.get_by_id(
        service_id,
    )