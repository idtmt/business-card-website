import pytest

from backend.core.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    ValidationError,
)
from backend.repositories.location_repository import LocationRepository
from backend.repositories.schedule_repository import ScheduleRepository
from backend.services.schedule_service import ScheduleService


@pytest.fixture
def schedule_service() -> ScheduleService:
    return ScheduleService(
        repository=ScheduleRepository(),
        location_repository=LocationRepository(),
    )


async def create_location() -> int:
    repository = LocationRepository()

    return await repository.create(
        title="Главный офис",
        address="ул. Амира Темура, 10",
        latitude=41.3111,
        longitude=69.2797,
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_schedule(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    schedule_id = await schedule_service.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    assert schedule_id > 0

    schedule = await schedule_service.get_by_id(
        schedule_id,
    )

    assert schedule == {
        "id": schedule_id,
        "location_id": location_id,
        "weekday": 0,
        "start_time": "09:00",
        "end_time": "18:00",
        "is_day_off": 0,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_schedule_normalizes_time(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    schedule_id = await schedule_service.create(
        location_id=location_id,
        weekday=0,
        start_time=" 9:5 ",
        end_time=" 18:30 ",
    )

    schedule = await schedule_service.get_by_id(
        schedule_id,
    )

    assert schedule["start_time"] == "09:05"
    assert schedule["end_time"] == "18:30"


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_day_off_schedule(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    schedule_id = await schedule_service.create(
        location_id=location_id,
        weekday=6,
        is_day_off=True,
    )

    schedule = await schedule_service.get_by_id(
        schedule_id,
    )

    assert schedule["weekday"] == 6
    assert schedule["start_time"] is None
    assert schedule["end_time"] is None
    assert schedule["is_day_off"] == 1


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "weekday",
    [-1, 7],
)
async def test_create_schedule_rejects_invalid_weekday(
    schedule_service: ScheduleService,
    test_database,
    weekday: int,
) -> None:
    location_id = await create_location()

    with pytest.raises(ValidationError):
        await schedule_service.create(
            location_id=location_id,
            weekday=weekday,
            start_time="09:00",
            end_time="18:00",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_schedule_rejects_invalid_location_id(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await schedule_service.create(
            location_id=0,
            weekday=0,
            start_time="09:00",
            end_time="18:00",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_schedule_raises_not_found_for_missing_location(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Локация не найдена",
    ):
        await schedule_service.create(
            location_id=999,
            weekday=0,
            start_time="09:00",
            end_time="18:00",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_schedule_rejects_duplicate_weekday(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    await schedule_service.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    with pytest.raises(
        AlreadyExistsError,
        match="Расписание для этого дня уже существует",
    ):
        await schedule_service.create(
            location_id=location_id,
            weekday=0,
            start_time="10:00",
            end_time="19:00",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_schedule_allows_same_weekday_for_different_locations(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    first_location_id = await create_location()

    second_location_repository = LocationRepository()

    second_location_id = await second_location_repository.create(
        title="Филиал",
        address="ул. Навои, 20",
        latitude=41.3,
        longitude=69.2,
    )

    first_schedule_id = await schedule_service.create(
        location_id=first_location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    second_schedule_id = await schedule_service.create(
        location_id=second_location_id,
        weekday=0,
        start_time="10:00",
        end_time="19:00",
    )

    assert first_schedule_id != second_schedule_id


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_schedule_requires_times_for_working_day(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    with pytest.raises(
        ValidationError,
        match="необходимо указать время начала",
    ):
        await schedule_service.create(
            location_id=location_id,
            weekday=0,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_schedule_rejects_times_for_day_off(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    with pytest.raises(
        ValidationError,
        match="время начала и окончания должно отсутствовать",
    ):
        await schedule_service.create(
            location_id=location_id,
            weekday=6,
            start_time="09:00",
            end_time="18:00",
            is_day_off=True,
        )


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "start_time,end_time",
    [
        ("25:00", "18:00"),
        ("09:60", "18:00"),
        ("abc", "18:00"),
        ("09", "18:00"),
        ("09:00", "abc"),
        ("09:00", "18"),
    ],
)
async def test_create_schedule_rejects_invalid_time(
    schedule_service: ScheduleService,
    test_database,
    start_time: str,
    end_time: str,
) -> None:
    location_id = await create_location()

    with pytest.raises(ValidationError):
        await schedule_service.create(
            location_id=location_id,
            weekday=0,
            start_time=start_time,
            end_time=end_time,
        )


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "start_time,end_time",
    [
        ("18:00", "09:00"),
        ("18:00", "18:00"),
    ],
)
async def test_create_schedule_rejects_invalid_time_range(
    schedule_service: ScheduleService,
    test_database,
    start_time: str,
    end_time: str,
) -> None:
    location_id = await create_location()

    with pytest.raises(
        ValidationError,
        match="Время окончания должно быть позже",
    ):
        await schedule_service.create(
            location_id=location_id,
            weekday=0,
            start_time=start_time,
            end_time=end_time,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_schedule_by_id(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    schedule_id = await schedule_service.create(
        location_id=location_id,
        weekday=2,
        start_time="10:00",
        end_time="19:00",
    )

    schedule = await schedule_service.get_by_id(
        schedule_id,
    )

    assert schedule["id"] == schedule_id
    assert schedule["weekday"] == 2


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_schedule_by_id_raises_not_found(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Расписание не найдено",
    ):
        await schedule_service.get_by_id(999)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_schedule_by_id_rejects_invalid_id(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await schedule_service.get_by_id(0)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_schedules_by_location(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    await schedule_service.create(
        location_id=location_id,
        weekday=2,
        start_time="10:00",
        end_time="19:00",
    )

    await schedule_service.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    schedules = await schedule_service.get_by_location(
        location_id,
    )

    assert [schedule["weekday"] for schedule in schedules] == [
        0,
        2,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_schedules_by_location_raises_not_found(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Локация не найдена",
    ):
        await schedule_service.get_by_location(999)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_schedule_by_location_and_weekday(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    schedule_id = await schedule_service.create(
        location_id=location_id,
        weekday=4,
        start_time="09:00",
        end_time="18:00",
    )

    schedule = await schedule_service.get_by_location_and_weekday(
        location_id=location_id,
        weekday=4,
    )

    assert schedule["id"] == schedule_id
    assert schedule["weekday"] == 4


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_schedule_by_location_and_weekday_raises_not_found(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    with pytest.raises(
        NotFoundError,
        match="Расписание для этого дня не найдено",
    ):
        await schedule_service.get_by_location_and_weekday(
            location_id=location_id,
            weekday=0,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_schedule(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    schedule_id = await schedule_service.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    await schedule_service.update(
        schedule_id=schedule_id,
        weekday=1,
        start_time="10:00",
        end_time="19:00",
        is_day_off=False,
    )

    schedule = await schedule_service.get_by_id(
        schedule_id,
    )

    assert schedule == {
        "id": schedule_id,
        "location_id": location_id,
        "weekday": 1,
        "start_time": "10:00",
        "end_time": "19:00",
        "is_day_off": 0,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_schedule_raises_not_found(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Расписание не найдено",
    ):
        await schedule_service.update(
            schedule_id=999,
            weekday=0,
            start_time="09:00",
            end_time="18:00",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_schedule_rejects_duplicate_weekday(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    first_schedule_id = await schedule_service.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    await schedule_service.create(
        location_id=location_id,
        weekday=1,
        start_time="10:00",
        end_time="19:00",
    )

    with pytest.raises(
        AlreadyExistsError,
        match="Расписание для этого дня уже существует",
    ):
        await schedule_service.update(
            schedule_id=first_schedule_id,
            weekday=1,
            start_time="11:00",
            end_time="20:00",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_schedule_allows_same_weekday(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    schedule_id = await schedule_service.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    await schedule_service.update(
        schedule_id=schedule_id,
        weekday=0,
        start_time="10:00",
        end_time="19:00",
    )

    schedule = await schedule_service.get_by_id(
        schedule_id,
    )

    assert schedule["weekday"] == 0
    assert schedule["start_time"] == "10:00"
    assert schedule["end_time"] == "19:00"


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_schedule(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    location_id = await create_location()

    schedule_id = await schedule_service.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    await schedule_service.delete(
        schedule_id,
    )

    with pytest.raises(NotFoundError):
        await schedule_service.get_by_id(
            schedule_id,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_schedule_raises_not_found(
    schedule_service: ScheduleService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Расписание не найдено",
    ):
        await schedule_service.delete(999)