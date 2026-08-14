from fastapi import APIRouter, Depends

from backend.api.dependencies import get_contact_service
from backend.api.schemas.contact import ContactResponse
from backend.services.contact_service import ContactService


router = APIRouter(
    prefix="/contacts",
    tags=["Public - Contacts"],
)


@router.get(
    "",
    response_model=list[ContactResponse],
)
async def get_contacts(
    service: ContactService = Depends(
        get_contact_service,
    ),
) -> list[dict]:
    return await service.get_all(
        is_hidden=False,
    )


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
)
async def get_contact(
    contact_id: int,
    service: ContactService = Depends(
        get_contact_service,
    ),
) -> dict:
    contact = await service.get_by_id(
        contact_id,
    )

    if contact["is_hidden"]:
        from backend.core.exceptions import NotFoundError

        raise NotFoundError(
            "Контакт не найден."
        )

    return contact