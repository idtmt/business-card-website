from typing import Any

from backend.core.exceptions import NotFoundError
from backend.repositories.service_repository import ServiceRepository
from backend.utils.validators import (
    normalize_optional,
    validate_id,
    validate_position,
    validate_required,
    validate_visibility,
)


class ServiceService:
    def __init__(
        self,
        repository: ServiceRepository,
    ) -> None:
        self.repository = repository

    async def create(
        self,
        name: str,
        description: str | None = None,
        position: int = 0,
        is_hidden: bool = False,
    ) -> int:
        name = validate_required(
            name,
            "name",
        )

        description = normalize_optional(
            description,
        )

        position = validate_position(
            position,
        )

        is_hidden = validate_visibility(
            is_hidden,
        )

        return await self.repository.create(
            name=name,
            description=description,
            position=position,
            is_hidden=is_hidden,
        )

    async def get_by_id(
        self,
        service_id: int,
    ) -> dict[str, Any]:
        service_id = validate_id(
            service_id,
            "service_id",
        )

        service = await self.repository.get_by_id(
            service_id,
        )

        if service is None:
            raise NotFoundError(
                "Услуга не найдена."
            )

        return service

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
        service_id: int,
        name: str,
        description: str | None = None,
        position: int = 0,
        is_hidden: bool = False,
    ) -> None:
        service_id = validate_id(
            service_id,
            "service_id",
        )

        name = validate_required(
            name,
            "name",
        )

        description = normalize_optional(
            description,
        )

        position = validate_position(
            position,
        )

        is_hidden = validate_visibility(
            is_hidden,
        )

        updated = await self.repository.update(
            service_id=service_id,
            name=name,
            description=description,
            position=position,
            is_hidden=is_hidden,
        )

        if not updated:
            raise NotFoundError(
                "Услуга не найдена."
            )

    async def delete(
        self,
        service_id: int,
    ) -> None:
        service_id = validate_id(
            service_id,
            "service_id",
        )

        deleted = await self.repository.delete(
            service_id,
        )

        if not deleted:
            raise NotFoundError(
                "Услуга не найдена."
            )