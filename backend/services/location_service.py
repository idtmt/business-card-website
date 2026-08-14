from typing import Any

from backend.core.exceptions import NotFoundError
from backend.repositories.location_repository import LocationRepository
from backend.utils.validators import (
    validate_bool,
    validate_id,
    validate_latitude,
    validate_longitude,
    validate_position,
    validate_required,
)


class LocationService:
    def __init__(
        self,
        repository: LocationRepository,
    ) -> None:
        self.repository = repository

    async def create(
        self,
        title: str,
        address: str,
        latitude: float,
        longitude: float,
        position: int = 0,
        is_hidden: bool = False,
    ) -> int:
        title = validate_required(
            title,
            "title",
        )

        address = validate_required(
            address,
            "address",
        )

        latitude = validate_latitude(
            latitude,
        )

        longitude = validate_longitude(
            longitude,
        )

        position = validate_position(
            position,
        )

        is_hidden = validate_bool(
            is_hidden,
            "is_hidden",
        )

        return await self.repository.create(
            title=title,
            address=address,
            latitude=latitude,
            longitude=longitude,
            position=position,
            is_hidden=is_hidden,
        )

    async def get_by_id(
        self,
        location_id: int,
    ) -> dict[str, Any]:
        location_id = validate_id(
            location_id,
            "location_id",
        )

        location = await self.repository.get_by_id(
            location_id,
        )

        if location is None:
            raise NotFoundError(
                "Локация не найдена."
            )

        return location

    async def get_all(
        self,
        is_hidden: bool | None = None,
    ) -> list[dict[str, Any]]:
        if is_hidden is not None:
            is_hidden = validate_bool(
                is_hidden,
                "is_hidden",
            )

        return await self.repository.get_all(
            is_hidden=is_hidden,
        )

    async def update(
        self,
        location_id: int,
        title: str,
        address: str,
        latitude: float,
        longitude: float,
        position: int = 0,
        is_hidden: bool = False,
    ) -> None:
        location_id = validate_id(
            location_id,
            "location_id",
        )

        title = validate_required(
            title,
            "title",
        )

        address = validate_required(
            address,
            "address",
        )

        latitude = validate_latitude(
            latitude,
        )

        longitude = validate_longitude(
            longitude,
        )

        position = validate_position(
            position,
        )

        is_hidden = validate_bool(
            is_hidden,
            "is_hidden",
        )

        updated = await self.repository.update(
            location_id=location_id,
            title=title,
            address=address,
            latitude=latitude,
            longitude=longitude,
            position=position,
            is_hidden=is_hidden,
        )

        if not updated:
            raise NotFoundError(
                "Локация не найдена."
            )

    async def delete(
        self,
        location_id: int,
    ) -> None:
        location_id = validate_id(
            location_id,
            "location_id",
        )

        deleted = await self.repository.delete(
            location_id,
        )

        if not deleted:
            raise NotFoundError(
                "Локация не найдена."
            )