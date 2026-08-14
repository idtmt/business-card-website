from typing import Any

from backend.core.exceptions import NotFoundError
from backend.repositories.location_repository import LocationRepository
from backend.repositories.schedule_repository import ScheduleRepository
from backend.utils.validators import validate_id


class PublicLocationService:
    def __init__(
        self,
        location_repository: LocationRepository,
        schedule_repository: ScheduleRepository,
    ) -> None:
        self.location_repository = location_repository
        self.schedule_repository = schedule_repository

    async def get_by_id(
        self,
        location_id: int,
    ) -> dict[str, Any]:
        location_id = validate_id(
            location_id,
            "location_id",
        )

        location = await self.location_repository.get_by_id(
            location_id,
        )

        if location is None or location["is_hidden"]:
            raise NotFoundError(
                "Локация не найдена."
            )

        schedules = await self.schedule_repository.get_by_location(
            location_id,
        )

        return self._build_public_location(
            location=location,
            schedules=schedules,
        )

    async def get_all(self) -> list[dict[str, Any]]:
        locations = await self.location_repository.get_all(
            is_hidden=False,
        )

        result = []

        for location in locations:
            schedules = await self.schedule_repository.get_by_location(
                location_id=location["id"],
            )

            result.append(
                self._build_public_location(
                    location=location,
                    schedules=schedules,
                )
            )

        return result

    @staticmethod
    def _build_public_location(
        location: dict[str, Any],
        schedules: list[dict[str, Any]],
    ) -> dict[str, Any]:
        return {
            "id": location["id"],
            "title": location["title"],
            "address": location["address"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "position": location["position"],
            "schedules": [
                {
                    "id": schedule["id"],
                    "location_id": schedule["location_id"],
                    "weekday": schedule["weekday"],
                    "start_time": schedule["start_time"],
                    "end_time": schedule["end_time"],
                    "is_day_off": schedule["is_day_off"],
                }
                for schedule in schedules
            ],
        }