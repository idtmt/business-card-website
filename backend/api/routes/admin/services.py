from fastapi import APIRouter, Depends, status

from backend.api.dependencies import get_service_service
from backend.api.schemas.service import (
    ServiceCreate,
    ServiceResponse,
    ServiceUpdate,
)
from backend.services.service_service import ServiceService


router = APIRouter(
    prefix="/services",
    tags=["Admin — Services"],
)


@router.post(
    "",
    response_model=int,
    status_code=status.HTTP_201_CREATED,
)
async def create_service(
    data: ServiceCreate,
    service: ServiceService = Depends(
        get_service_service,
    ),
):
    return await service.create(
        name=data.name,
        description=data.description,
        position=data.position,
        is_hidden=data.is_hidden,
    )


@router.get(
    "/{service_id}",
    response_model=ServiceResponse,
)
async def get_service(
    service_id: int,
    service: ServiceService = Depends(
        get_service_service,
    ),
):
    return await service.get_by_id(
        service_id,
    )


@router.get(
    "",
    response_model=list[ServiceResponse],
)
async def get_services(
    is_hidden: bool | None = None,
    service: ServiceService = Depends(
        get_service_service,
    ),
):
    return await service.get_all(
        is_hidden=is_hidden,
    )


@router.put(
    "/{service_id}",
)
async def update_service(
    service_id: int,
    data: ServiceUpdate,
    service: ServiceService = Depends(
        get_service_service,
    ),
):
    await service.update(
        service_id=service_id,
        name=data.name,
        description=data.description,
        position=data.position,
        is_hidden=data.is_hidden,
    )

    return {
        "message": "Услуга обновлена."
    }


@router.delete(
    "/{service_id}",
)
async def delete_service(
    service_id: int,
    service: ServiceService = Depends(
        get_service_service,
    ),
):
    await service.delete(
        service_id,
    )

    return {
        "message": "Услуга удалена."
    }