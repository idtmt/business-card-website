from fastapi import APIRouter, Depends

from backend.api.dependencies import get_faq_service
from backend.api.schemas.faq import FaqResponse
from backend.services.faq_service import FaqService


router = APIRouter(
    prefix="/faq",
    tags=["Public - FAQ"],
)


@router.get(
    "",
    response_model=list[FaqResponse],
)
async def get_faq(
    service: FaqService = Depends(
        get_faq_service,
    ),
) -> list[dict]:
    return await service.get_all(
        is_hidden=False,
    )


@router.get(
    "/{faq_id}",
    response_model=FaqResponse,
)
async def get_faq_item(
    faq_id: int,
    service: FaqService = Depends(
        get_faq_service,
    ),
) -> dict:
    faq = await service.get_by_id(
        faq_id,
    )

    if faq["is_hidden"]:
        from backend.core.exceptions import NotFoundError

        raise NotFoundError(
            "FAQ не найден."
        )

    return faq