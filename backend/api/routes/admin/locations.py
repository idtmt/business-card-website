from fastapi import APIRouter, Depends, status

from backend.api.dependencies import get_location_service
from backend.api.schemas.location import (
    LocationCreate,
    LocationResponse,
    LocationUpdate,
)
from backend.services.location_service import LocationService


router = APIRouter(
    prefix="/locations",
    tags=["Admin — Locations"],
)


@router.post(
    "",
    response_model=int,
    status_code=status.HTTP_201_CREATED,
)
async def create_location(
    data: LocationCreate,
    service: LocationService = Depends(
        get_location_service,
    ),
):
    return await service.create(
        title=data.title,
        address=data.address,
        latitude=data.latitude,
        longitude=data.longitude,
        position=data.position,
        is_hidden=data.is_hidden,
    )


@router.get(
    "/{location_id}",
    response_model=LocationResponse,
)
async def get_location(
    location_id: int,
    service: LocationService = Depends(
        get_location_service,
    ),
):
    return await service.get_by_id(
        location_id,
    )


@router.get(
    "",
    response_model=list[LocationResponse],
)
async def get_locations(
    is_hidden: bool | None = None,
    service: LocationService = Depends(
        get_location_service,
    ),
):
    return await service.get_all(
        is_hidden=is_hidden,
    )


@router.put(
    "/{location_id}",
)
async def update_location(
    location_id: int,
    data: LocationUpdate,
    service: LocationService = Depends(
        get_location_service,
    ),
):
    await service.update(
        location_id=location_id,
        title=data.title,
        address=data.address,
        latitude=data.latitude,
        longitude=data.longitude,
        position=data.position,
        is_hidden=data.is_hidden,
    )

    return {
        "message": "Локация обновлена."
    }


@router.delete(
    "/{location_id}",
)
async def delete_location(
    location_id: int,
    service: LocationService = Depends(
        get_location_service,
    ),
):
    await service.delete(
        location_id,
    )

    return {
        "message": "Локация удалена."
    }