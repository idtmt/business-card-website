import pytest

from backend.repositories.schedule_repository import ScheduleRepository
from backend.repositories.location_repository import LocationRepository


@pytest.fixture
async def location_id(test_database):
    repository = LocationRepository()

    return await repository.create(
        title="Основной филиал",
        address="Ташкент",
        latitude=41.311081,
        longitude=69.240562,
    )


@pytest.mark.repository
async def test_create_returns_id(
    test_database,
    location_id,
):
    repository = ScheduleRepository()

    schedule_id = await repository.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    assert schedule_id == 1


@pytest.mark.repository
async def test_create_saves_schedule(
    test_database,
    location_id,
):
    repository = ScheduleRepository()

    schedule_id = await repository.create(
        location_id=location_id,
        weekday=1,
        start_time="10:00",
        end_time="19:00",
    )

    schedule = await repository.get_by_id(schedule_id)

    assert schedule == {
        "id": schedule_id,
        "location_id": location_id,
        "weekday": 1,
        "start_time": "10:00",
        "end_time": "19:00",
        "is_day_off": 0,
    }


@pytest.mark.repository
async def test_create_saves_day_off(
    test_database,
    location_id,
):
    repository = ScheduleRepository()

    schedule_id = await repository.create(
        location_id=location_id,
        weekday=6,
        is_day_off=True,
    )

    schedule = await repository.get_by_id(schedule_id)

    assert schedule is not None
    assert schedule["is_day_off"] == 1
    assert schedule["start_time"] is None
    assert schedule["end_time"] is None


@pytest.mark.repository
async def test_get_by_id_returns_existing_schedule(
    test_database,
    location_id,
):
    repository = ScheduleRepository()

    schedule_id = await repository.create(
        location_id=location_id,
        weekday=2,
        start_time="09:30",
        end_time="18:30",
    )

    result = await repository.get_by_id(schedule_id)

    assert result is not None
    assert result["id"] == schedule_id
    assert result["location_id"] == location_id
    assert result["weekday"] == 2
    assert result["start_time"] == "09:30"
    assert result["end_time"] == "18:30"
    assert result["is_day_off"] == 0


@pytest.mark.repository
async def test_get_by_id_returns_none_for_missing_schedule(
    test_database,
):
    repository = ScheduleRepository()

    result = await repository.get_by_id(999)

    assert result is None


@pytest.mark.repository
async def test_get_by_location_returns_schedules_in_weekday_order(
    test_database,
    location_id,
):
    repository = ScheduleRepository()

    await repository.create(
        location_id=location_id,
        weekday=4,
        start_time="09:00",
        end_time="18:00",
    )

    await repository.create(
        location_id=location_id,
        weekday=1,
        start_time="10:00",
        end_time="19:00",
    )

    await repository.create(
        location_id=location_id,
        weekday=3,
        start_time="09:30",
        end_time="18:30",
    )

    schedules = await repository.get_by_location(
        location_id,
    )

    assert [schedule["weekday"] for schedule in schedules] == [
        1,
        3,
        4,
    ]


@pytest.mark.repository
async def test_get_by_location_returns_only_schedules_of_location(
    test_database,
):
    location_repository = LocationRepository()
    schedule_repository = ScheduleRepository()

    first_location_id = await location_repository.create(
        title="Первый филиал",
        address="Адрес 1",
        latitude=41.1,
        longitude=69.1,
    )

    second_location_id = await location_repository.create(
        title="Второй филиал",
        address="Адрес 2",
        latitude=41.2,
        longitude=69.2,
    )

    first_schedule_id = await schedule_repository.create(
        location_id=first_location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    await schedule_repository.create(
        location_id=second_location_id,
        weekday=0,
        start_time="10:00",
        end_time="19:00",
    )

    schedules = await schedule_repository.get_by_location(
        first_location_id,
    )

    assert [schedule["id"] for schedule in schedules] == [
        first_schedule_id,
    ]


@pytest.mark.repository
async def test_get_by_location_returns_empty_list_for_location_without_schedules(
    test_database,
    location_id,
):
    repository = ScheduleRepository()

    result = await repository.get_by_location(
        location_id,
    )

    assert result == []


@pytest.mark.repository
async def test_get_by_location_and_weekday_returns_schedule(
    test_database,
    location_id,
):
    repository = ScheduleRepository()

    schedule_id = await repository.create(
        location_id=location_id,
        weekday=2,
        start_time="09:00",
        end_time="18:00",
    )

    result = await repository.get_by_location_and_weekday(
        location_id=location_id,
        weekday=2,
    )

    assert result is not None
    assert result["id"] == schedule_id
    assert result["weekday"] == 2


@pytest.mark.repository
async def test_get_by_location_and_weekday_returns_none_when_missing(
    test_database,
    location_id,
):
    repository = ScheduleRepository()

    result = await repository.get_by_location_and_weekday(
        location_id=location_id,
        weekday=5,
    )

    assert result is None


@pytest.mark.repository
async def test_get_by_location_and_weekday_does_not_return_schedule_from_another_location(
    test_database,
):
    location_repository = LocationRepository()
    schedule_repository = ScheduleRepository()

    first_location_id = await location_repository.create(
        title="Первый филиал",
        address="Адрес 1",
        latitude=41.1,
        longitude=69.1,
    )

    second_location_id = await location_repository.create(
        title="Второй филиал",
        address="Адрес 2",
        latitude=41.2,
        longitude=69.2,
    )

    await schedule_repository.create(
        location_id=first_location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    result = await schedule_repository.get_by_location_and_weekday(
        location_id=second_location_id,
        weekday=0,
    )

    assert result is None


@pytest.mark.repository
async def test_update_updates_existing_schedule(
    test_database,
    location_id,
):
    repository = ScheduleRepository()

    schedule_id = await repository.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    result = await repository.update(
        schedule_id=schedule_id,
        weekday=5,
        start_time="10:00",
        end_time="20:00",
        is_day_off=False,
    )

    assert result is True

    schedule = await repository.get_by_id(schedule_id)

    assert schedule is not None
    assert schedule["weekday"] == 5
    assert schedule["start_time"] == "10:00"
    assert schedule["end_time"] == "20:00"
    assert schedule["is_day_off"] == 0


@pytest.mark.repository
async def test_update_can_set_day_off(
    test_database,
    location_id,
):
    repository = ScheduleRepository()

    schedule_id = await repository.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    result = await repository.update(
        schedule_id=schedule_id,
        weekday=0,
        is_day_off=True,
    )

    assert result is True

    schedule = await repository.get_by_id(schedule_id)

    assert schedule is not None
    assert schedule["is_day_off"] == 1
    assert schedule["start_time"] is None
    assert schedule["end_time"] is None


@pytest.mark.repository
async def test_update_returns_false_for_missing_schedule(
    test_database,
):
    repository = ScheduleRepository()

    result = await repository.update(
        schedule_id=999,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    assert result is False


@pytest.mark.repository
async def test_delete_removes_existing_schedule(
    test_database,
    location_id,
):
    repository = ScheduleRepository()

    schedule_id = await repository.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    result = await repository.delete(schedule_id)

    assert result is True
    assert await repository.get_by_id(schedule_id) is None


@pytest.mark.repository
async def test_delete_returns_false_for_missing_schedule(
    test_database,
):
    repository = ScheduleRepository()

    result = await repository.delete(999)

    assert result is False