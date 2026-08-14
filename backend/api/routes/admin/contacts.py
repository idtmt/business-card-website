from fastapi import APIRouter, Depends, status

from backend.api.dependencies import get_contact_service
from backend.api.schemas.contact import (
    ContactCreate,
    ContactResponse,
    ContactUpdate,
)
from backend.services.contact_service import ContactService


router = APIRouter(
    prefix="/contacts",
    tags=["Admin — Contacts"],
)


@router.post(
    "",
    response_model=int,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
    data: ContactCreate,
    service: ContactService = Depends(
        get_contact_service,
    ),
):
    return await service.create(
        title=data.title,
        value=data.value,
        url=data.url,
        icon=data.icon,
        position=data.position,
        is_hidden=data.is_hidden,
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
):
    return await service.get_by_id(
        contact_id,
    )


@router.get(
    "",
    response_model=list[ContactResponse],
)
async def get_contacts(
    is_hidden: bool | None = None,
    service: ContactService = Depends(
        get_contact_service,
    ),
):
    return await service.get_all(
        is_hidden=is_hidden,
    )


@router.put(
    "/{contact_id}",
)
async def update_contact(
    contact_id: int,
    data: ContactUpdate,
    service: ContactService = Depends(
        get_contact_service,
    ),
):
    await service.update(
        contact_id=contact_id,
        title=data.title,
        value=data.value,
        url=data.url,
        icon=data.icon,
        position=data.position,
        is_hidden=data.is_hidden,
    )

    return {
        "message": "Контакт обновлен."
    }


@router.delete(
    "/{contact_id}",
)
async def delete_contact(
    contact_id: int,
    service: ContactService = Depends(
        get_contact_service,
    ),
):
    await service.delete(
        contact_id,
    )

    return {
        "message": "Контакт удален."
    }