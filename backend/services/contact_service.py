from typing import Any

from backend.core.exceptions import NotFoundError
from backend.repositories.contact_repository import ContactRepository
from backend.utils.validators import (
    normalize_optional,
    validate_id,
    validate_position,
    validate_required,
    validate_visibility,
)


class ContactService:
    def __init__(
        self,
        repository: ContactRepository,
    ) -> None:
        self.repository = repository

    async def create(
        self,
        title: str,
        value: str,
        url: str | None = None,
        icon: str | None = None,
        position: int = 0,
        is_hidden: bool = False,
    ) -> int:
        title = validate_required(
            title,
            "title",
        )

        value = validate_required(
            value,
            "value",
        )

        url = normalize_optional(url)
        icon = normalize_optional(icon)

        position = validate_position(
            position,
        )

        is_hidden = validate_visibility(
            is_hidden,
        )

        return await self.repository.create(
            title=title,
            value=value,
            url=url,
            icon=icon,
            position=position,
            is_hidden=is_hidden,
        )

    async def get_by_id(
        self,
        contact_id: int,
    ) -> dict[str, Any]:
        contact_id = validate_id(
            contact_id,
            "contact_id",
        )

        contact = await self.repository.get_by_id(
            contact_id,
        )

        if contact is None:
            raise NotFoundError(
                "Контакт не найден."
            )

        return contact

    async def get_all(
        self,
        is_hidden: bool | None = None,
    ) -> list[dict[str, Any]]:
        if is_hidden is not None:
            is_hidden = validate_visibility(
                is_hidden,
            )

        return await self.repository.get_all(
            is_hidden=is_hidden,
        )

    async def update(
        self,
        contact_id: int,
        title: str,
        value: str,
        url: str | None = None,
        icon: str | None = None,
        position: int = 0,
        is_hidden: bool = False,
    ) -> None:
        contact_id = validate_id(
            contact_id,
            "contact_id",
        )

        title = validate_required(
            title,
            "title",
        )

        value = validate_required(
            value,
            "value",
        )

        url = normalize_optional(url)
        icon = normalize_optional(icon)

        position = validate_position(
            position,
        )

        is_hidden = validate_visibility(
            is_hidden,
        )

        updated = await self.repository.update(
            contact_id=contact_id,
            title=title,
            value=value,
            url=url,
            icon=icon,
            position=position,
            is_hidden=is_hidden,
        )

        if not updated:
            raise NotFoundError(
                "Контакт не найден."
            )

    async def delete(
        self,
        contact_id: int,
    ) -> None:
        contact_id = validate_id(
            contact_id,
            "contact_id",
        )

        deleted = await self.repository.delete(
            contact_id,
        )

        if not deleted:
            raise NotFoundError(
                "Контакт не найден."
            )