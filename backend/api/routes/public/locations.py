from fastapi import APIRouter, Depends

from backend.api.dependencies import get_public_location_service
from backend.api.schemas.public_location import PublicLocationResponse
from backend.services.public_location_service import PublicLocationService


router = APIRouter(
    prefix="/locations",
    tags=["Public Locations"],
)


@router.get(
    "",
    response_model=list[PublicLocationResponse],
)
async def get_locations(
    service: PublicLocationService = Depends(
        get_public_location_service,
    ),
) -> list[PublicLocationResponse]:
    return await service.get_all()


@router.get(
    "/{location_id}",
    response_model=PublicLocationResponse,
)
async def get_location(
    location_id: int,
    service: PublicLocationService = Depends(
        get_public_location_service,
    ),
) -> PublicLocationResponse:
    return await service.get_by_id(
        location_id,
    )