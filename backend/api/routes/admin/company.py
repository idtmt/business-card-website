from fastapi import APIRouter, Depends, status

from backend.api.dependencies import get_company_service
from backend.api.schemas.company import (
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
)
from backend.services.company_service import CompanyService


router = APIRouter(
    prefix="/company",
    tags=["Admin — Company"]
)


@router.get(
    "",
    response_model=CompanyResponse | None,
)
async def get_company(
    service: CompanyService = Depends(
        get_company_service,
    ),
):
    return await service.get()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_company(
    data: CompanyCreate,
    service: CompanyService = Depends(
        get_company_service,
    ),
):
    await service.create(
        name=data.name,
        description=data.description,
    )

    return {
        "message": "Информация о компании создана."
    }


@router.put(
    "",
)
async def update_company(
    data: CompanyUpdate,
    service: CompanyService = Depends(
        get_company_service,
    ),
):
    await service.update(
        name=data.name,
        description=data.description,
    )

    return {
        "message": "Информация о компании обновлена."
    }