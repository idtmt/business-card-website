from typing import Any

from backend.core.exceptions import NotFoundError
from backend.repositories.price_repository import PriceRepository
from backend.repositories.service_repository import ServiceRepository
from backend.utils.validators import (
    validate_id,
    validate_position,
    validate_required,
    validate_visibility,
)


class PriceService:
    def __init__(
        self,
        repository: PriceRepository,
        service_repository: ServiceRepository,
    ) -> None:
        self.repository = repository
        self.service_repository = service_repository

    async def create(
        self,
        service_id: int,
        title: str,
        price: str,
        position: int = 0,
        is_hidden: bool = False,
    ) -> int:
        service_id = validate_id(
            service_id,
            "service_id",
        )

        title = validate_required(
            title,
            "title",
        )

        price = validate_required(
            price,
            "price",
        )

        position = validate_position(
            position,
        )

        is_hidden = validate_visibility(
            is_hidden,
        )

        await self._ensure_service_exists(
            service_id,
        )

        return await self.repository.create(
            service_id=service_id,
            title=title,
            price=price,
            position=position,
            is_hidden=is_hidden,
        )

    async def get_by_id(
        self,
        price_id: int,
    ) -> dict[str, Any]:
        price_id = validate_id(
            price_id,
            "price_id",
        )

        price = await self.repository.get_by_id(
            price_id,
        )

        if price is None:
            raise NotFoundError(
                "Цена не найдена."
            )

        return price

    async def get_by_service(
        self,
        service_id: int,
        is_hidden: bool | None = None,
    ) -> list[dict[str, Any]]:
        service_id = validate_id(
            service_id,
            "service_id",
        )

        if is_hidden is not None:
            is_hidden = validate_visibility(
                is_hidden,
            )

        await self._ensure_service_exists(
            service_id,
        )

        return await self.repository.get_by_service(
            service_id=service_id,
            is_hidden=is_hidden,
        )

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
        price_id: int,
        title: str,
        price: str,
        position: int = 0,
        is_hidden: bool = False,
    ) -> None:
        price_id = validate_id(
            price_id,
            "price_id",
        )

        title = validate_required(
            title,
            "title",
        )

        price = validate_required(
            price,
            "price",
        )

        position = validate_position(
            position,
        )

        is_hidden = validate_visibility(
            is_hidden,
        )

        updated = await self.repository.update(
            price_id=price_id,
            title=title,
            price=price,
            position=position,
            is_hidden=is_hidden,
        )

        if not updated:
            raise NotFoundError(
                "Цена не найдена."
            )

    async def delete(
        self,
        price_id: int,
    ) -> None:
        price_id = validate_id(
            price_id,
            "price_id",
        )

        deleted = await self.repository.delete(
            price_id,
        )

        if not deleted:
            raise NotFoundError(
                "Цена не найдена."
            )

    async def _ensure_service_exists(
        self,
        service_id: int,
    ) -> None:
        service = await self.service_repository.get_by_id(
            service_id,
        )

        if service is None:
            raise NotFoundError(
                "Услуга не найдена."
            )