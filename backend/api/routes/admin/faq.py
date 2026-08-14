from fastapi import APIRouter, Depends, status

from backend.api.dependencies import get_faq_service
from backend.api.schemas.faq import (
    FaqCreate,
    FaqResponse,
    FaqUpdate,
)
from backend.services.faq_service import FaqService


router = APIRouter(
    prefix="/faq",
    tags=["Admin — FAQ"],
)


@router.post(
    "",
    response_model=int,
    status_code=status.HTTP_201_CREATED,
)
async def create_faq(
    data: FaqCreate,
    service: FaqService = Depends(
        get_faq_service,
    ),
):
    return await service.create(
        question=data.question,
        answer=data.answer,
        position=data.position,
        is_hidden=data.is_hidden,
    )


@router.get(
    "/{faq_id}",
    response_model=FaqResponse,
)
async def get_faq(
    faq_id: int,
    service: FaqService = Depends(
        get_faq_service,
    ),
):
    return await service.get_by_id(
        faq_id,
    )


@router.get(
    "",
    response_model=list[FaqResponse],
)
async def get_faqs(
    is_hidden: bool | None = None,
    service: FaqService = Depends(
        get_faq_service,
    ),
):
    return await service.get_all(
        is_hidden=is_hidden,
    )


@router.put(
    "/{faq_id}",
)
async def update_faq(
    faq_id: int,
    data: FaqUpdate,
    service: FaqService = Depends(
        get_faq_service,
    ),
):
    await service.update(
        faq_id=faq_id,
        question=data.question,
        answer=data.answer,
        position=data.position,
        is_hidden=data.is_hidden,
    )

    return {
        "message": "FAQ обновлен."
    }


@router.delete(
    "/{faq_id}",
)
async def delete_faq(
    faq_id: int,
    service: FaqService = Depends(
        get_faq_service,
    ),
):
    await service.delete(
        faq_id,
    )

    return {
        "message": "FAQ удален."
    }