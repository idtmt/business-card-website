from typing import Any

from backend.core.exceptions import NotFoundError
from backend.repositories.price_repository import PriceRepository
from backend.repositories.service_repository import ServiceRepository
from backend.utils.validators import validate_id


class PublicServiceService:
    def __init__(
        self,
        service_repository: ServiceRepository,
        price_repository: PriceRepository,
    ) -> None:
        self.service_repository = service_repository
        self.price_repository = price_repository

    async def get_by_id(
        self,
        service_id: int,
    ) -> dict[str, Any]:
        service_id = validate_id(
            service_id,
            "service_id",
        )

        service = await self.service_repository.get_by_id(
            service_id,
        )

        if service is None or service["is_hidden"]:
            raise NotFoundError(
                "Услуга не найдена."
            )

        prices = await self.price_repository.get_by_service(
            service_id=service_id,
            is_hidden=False,
        )

        return self._build_public_service(
            service=service,
            prices=prices,
        )

    async def get_all(self) -> list[dict[str, Any]]:
        services = await self.service_repository.get_all(
            is_hidden=False,
        )

        result = []

        for service in services:
            prices = await self.price_repository.get_by_service(
                service_id=service["id"],
                is_hidden=False,
            )

            result.append(
                self._build_public_service(
                    service=service,
                    prices=prices,
                )
            )

        return result

    @classmethod
    def _build_public_service(
        cls,
        service: dict[str, Any],
        prices: list[dict[str, Any]],
    ) -> dict[str, Any]:
        return {
            "id": service["id"],
            "name": service["name"],
            "description": service["description"],
            "position": service["position"],
            "prices": [
                cls._build_public_price(price)
                for price in prices
            ],
        }

    @staticmethod
    def _build_public_price(
        price: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "id": price["id"],
            "service_id": price["service_id"],
            "title": price["title"],
            "price": price["price"],
            "position": price["position"],
        }