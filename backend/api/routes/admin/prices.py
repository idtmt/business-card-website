from fastapi import APIRouter, Depends, status

from backend.api.dependencies import get_price_service
from backend.api.schemas.price import (
    PriceCreate,
    PriceResponse,
    PriceUpdate,
)
from backend.services.price_service import PriceService


router = APIRouter(
    prefix="/prices",
    tags=["Admin — Prices"],
)


@router.post(
    "",
    response_model=int,
    status_code=status.HTTP_201_CREATED,
)
async def create_price(
    data: PriceCreate,
    service: PriceService = Depends(
        get_price_service,
    ),
):
    return await service.create(
        service_id=data.service_id,
        title=data.title,
        price=data.price,
        position=data.position,
        is_hidden=data.is_hidden,
    )


@router.get(
    "/{price_id}",
    response_model=PriceResponse,
)
async def get_price(
    price_id: int,
    service: PriceService = Depends(
        get_price_service,
    ),
):
    return await service.get_by_id(
        price_id,
    )


@router.get(
    "/service/{service_id}",
    response_model=list[PriceResponse],
)
async def get_prices_by_service(
    service_id: int,
    is_hidden: bool | None = None,
    service: PriceService = Depends(
        get_price_service,
    ),
):
    return await service.get_by_service(
        service_id=service_id,
        is_hidden=is_hidden,
    )


@router.get(
    "",
    response_model=list[PriceResponse],
)
async def get_prices(
    is_hidden: bool | None = None,
    service: PriceService = Depends(
        get_price_service,
    ),
):
    return await service.get_all(
        is_hidden=is_hidden,
    )


@router.put(
    "/{price_id}",
)
async def update_price(
    price_id: int,
    data: PriceUpdate,
    service: PriceService = Depends(
        get_price_service,
    ),
):
    await service.update(
        price_id=price_id,
        title=data.title,
        price=data.price,
        position=data.position,
        is_hidden=data.is_hidden,
    )

    return {
        "message": "Цена обновлена."
    }


@router.delete(
    "/{price_id}",
)
async def delete_price(
    price_id: int,
    service: PriceService = Depends(
        get_price_service,
    ),
):
    await service.delete(
        price_id,
    )

    return {
        "message": "Цена удалена."
    }