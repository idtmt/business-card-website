from typing import Any

from backend.core.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    ValidationError,
)
from backend.repositories.location_repository import LocationRepository
from backend.repositories.schedule_repository import ScheduleRepository
from backend.utils.validators import (
    validate_bool,
    validate_id,
    validate_time,
    validate_weekday,
)


class ScheduleService:
    def __init__(
        self,
        repository: ScheduleRepository,
        location_repository: LocationRepository,
    ) -> None:
        self.repository = repository
        self.location_repository = location_repository

    async def create(
        self,
        location_id: int,
        weekday: int,
        start_time: str | None = None,
        end_time: str | None = None,
        is_day_off: bool = False,
    ) -> int:
        location_id = validate_id(
            location_id,
            "location_id",
        )

        weekday = validate_weekday(
            weekday,
        )

        is_day_off = validate_bool(
            is_day_off,
            "is_day_off",
        )

        start_time, end_time = self._validate_schedule_times(
            start_time=start_time,
            end_time=end_time,
            is_day_off=is_day_off,
        )

        await self._ensure_location_exists(
            location_id,
        )

        existing = await self.repository.get_by_location_and_weekday(
            location_id=location_id,
            weekday=weekday,
        )

        if existing is not None:
            raise AlreadyExistsError(
                "Расписание для этого дня уже существует."
            )

        return await self.repository.create(
            location_id=location_id,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time,
            is_day_off=is_day_off,
        )

    async def get_by_id(
        self,
        schedule_id: int,
    ) -> dict[str, Any]:
        schedule_id = validate_id(
            schedule_id,
            "schedule_id",
        )

        schedule = await self.repository.get_by_id(
            schedule_id,
        )

        if schedule is None:
            raise NotFoundError(
                "Расписание не найдено."
            )

        return schedule

    async def get_by_location(
        self,
        location_id: int,
    ) -> list[dict[str, Any]]:
        location_id = validate_id(
            location_id,
            "location_id",
        )

        await self._ensure_location_exists(
            location_id,
        )

        return await self.repository.get_by_location(
            location_id,
        )

    async def get_by_location_and_weekday(
        self,
        location_id: int,
        weekday: int,
    ) -> dict[str, Any]:
        location_id = validate_id(
            location_id,
            "location_id",
        )

        weekday = validate_weekday(
            weekday,
        )

        await self._ensure_location_exists(
            location_id,
        )

        schedule = await self.repository.get_by_location_and_weekday(
            location_id=location_id,
            weekday=weekday,
        )

        if schedule is None:
            raise NotFoundError(
                "Расписание для этого дня не найдено."
            )

        return schedule

    async def update(
        self,
        schedule_id: int,
        weekday: int,
        start_time: str | None = None,
        end_time: str | None = None,
        is_day_off: bool = False,
    ) -> None:
        schedule_id = validate_id(
            schedule_id,
            "schedule_id",
        )

        weekday = validate_weekday(
            weekday,
        )

        is_day_off = validate_bool(
            is_day_off,
            "is_day_off",
        )

        start_time, end_time = self._validate_schedule_times(
            start_time=start_time,
            end_time=end_time,
            is_day_off=is_day_off,
        )

        current = await self.repository.get_by_id(
            schedule_id,
        )

        if current is None:
            raise NotFoundError(
                "Расписание не найдено."
            )

        existing = await self.repository.get_by_location_and_weekday(
            location_id=current["location_id"],
            weekday=weekday,
        )

        if existing is not None and existing["id"] != schedule_id:
            raise AlreadyExistsError(
                "Расписание для этого дня уже существует."
            )

        updated = await self.repository.update(
            schedule_id=schedule_id,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time,
            is_day_off=is_day_off,
        )

        if not updated:
            raise NotFoundError(
                "Расписание не найдено."
            )

    async def delete(
        self,
        schedule_id: int,
    ) -> None:
        schedule_id = validate_id(
            schedule_id,
            "schedule_id",
        )

        deleted = await self.repository.delete(
            schedule_id,
        )

        if not deleted:
            raise NotFoundError(
                "Расписание не найдено."
            )

    async def _ensure_location_exists(
        self,
        location_id: int,
    ) -> None:
        location = await self.location_repository.get_by_id(
            location_id,
        )

        if location is None:
            raise NotFoundError(
                "Локация не найдена."
            )

    @staticmethod
    def _validate_schedule_times(
        start_time: str | None,
        end_time: str | None,
        is_day_off: bool,
    ) -> tuple[str | None, str | None]:
        if is_day_off:
            if start_time is not None or end_time is not None:
                raise ValidationError(
                    "Для выходного дня время начала и окончания "
                    "должно отсутствовать."
                )

            return None, None

        if start_time is None or end_time is None:
            raise ValidationError(
                "Для рабочего дня необходимо указать время начала "
                "и окончания."
            )

        start_time = validate_time(
            start_time,
            "start_time",
        )

        end_time = validate_time(
            end_time,
            "end_time",
        )

        if start_time >= end_time:
            raise ValidationError(
                "Время окончания должно быть позже времени начала."
            )

        return start_time, end_time