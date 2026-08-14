from fastapi import APIRouter, Depends

from backend.api.dependencies import get_company_service
from backend.api.schemas.company import CompanyResponse
from backend.services.company_service import CompanyService


router = APIRouter(
    prefix="/company",
    tags=["Public - Company"],
)


@router.get(
    "",
    response_model=CompanyResponse | None,
)
async def get_company(
    service: CompanyService = Depends(
        get_company_service,
    ),
) -> CompanyResponse | None:
    return await service.get()