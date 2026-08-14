import pytest

from backend.repositories.location_repository import LocationRepository


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_returns_id(test_database):
    repository = LocationRepository()

    location_id = await repository.create(
        title="Основной офис",
        address="Ташкент, ул. Амира Темура, 1",
        latitude=41.311081,
        longitude=69.240562,
    )

    assert location_id == 1


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_saves_hidden_status(test_database):
    repository = LocationRepository()

    location_id = await repository.create(
        title="Скрытый филиал",
        address="Ташкент",
        latitude=41.311081,
        longitude=69.240562,
        is_hidden=True,
    )

    location = await repository.get_by_id(location_id)

    assert location is not None
    assert location["is_hidden"] == 1


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_id_returns_existing_location(test_database):
    repository = LocationRepository()

    location_id = await repository.create(
        title="Основной офис",
        address="Ташкент, ул. Амира Темура, 1",
        latitude=41.311081,
        longitude=69.240562,
    )

    result = await repository.get_by_id(location_id)

    assert result == {
        "id": location_id,
        "title": "Основной офис",
        "address": "Ташкент, ул. Амира Темура, 1",
        "latitude": 41.311081,
        "longitude": 69.240562,
        "position": 0,
        "is_hidden": 0,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_missing_location(
    test_database,
):
    repository = LocationRepository()

    result = await repository.get_by_id(999)

    assert result is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_returns_locations_in_position_order(
    test_database,
):
    repository = LocationRepository()

    first_id = await repository.create(
        title="Второй",
        address="Адрес 2",
        latitude=41.2,
        longitude=69.2,
        position=2,
    )

    second_id = await repository.create(
        title="Первый",
        address="Адрес 1",
        latitude=41.1,
        longitude=69.1,
        position=1,
    )

    locations = await repository.get_all()

    assert [location["id"] for location in locations] == [
        second_id,
        first_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_filters_hidden_locations(test_database):
    repository = LocationRepository()

    visible_id = await repository.create(
        title="Видимый",
        address="Адрес 1",
        latitude=41.1,
        longitude=69.1,
        is_hidden=False,
    )

    await repository.create(
        title="Скрытый",
        address="Адрес 2",
        latitude=41.2,
        longitude=69.2,
        is_hidden=True,
    )

    locations = await repository.get_all(is_hidden=False)

    assert [location["id"] for location in locations] == [
        visible_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_returns_only_hidden_locations(test_database):
    repository = LocationRepository()

    await repository.create(
        title="Видимый",
        address="Адрес 1",
        latitude=41.1,
        longitude=69.1,
        is_hidden=False,
    )

    hidden_id = await repository.create(
        title="Скрытый",
        address="Адрес 2",
        latitude=41.2,
        longitude=69.2,
        is_hidden=True,
    )

    locations = await repository.get_all(is_hidden=True)

    assert [location["id"] for location in locations] == [
        hidden_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_updates_existing_location(test_database):
    repository = LocationRepository()

    location_id = await repository.create(
        title="Старое название",
        address="Старый адрес",
        latitude=41.1,
        longitude=69.1,
    )

    result = await repository.update(
        location_id=location_id,
        title="Новое название",
        address="Новый адрес",
        latitude=41.311081,
        longitude=69.240562,
        position=5,
        is_hidden=True,
    )

    assert result is True

    location = await repository.get_by_id(location_id)

    assert location == {
        "id": location_id,
        "title": "Новое название",
        "address": "Новый адрес",
        "latitude": 41.311081,
        "longitude": 69.240562,
        "position": 5,
        "is_hidden": 1,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_returns_false_for_missing_location(
    test_database,
):
    repository = LocationRepository()

    result = await repository.update(
        location_id=999,
        title="Название",
        address="Адрес",
        latitude=41.3,
        longitude=69.2,
    )

    assert result is False


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_removes_existing_location(test_database):
    repository = LocationRepository()

    location_id = await repository.create(
        title="Филиал",
        address="Ташкент",
        latitude=41.3,
        longitude=69.2,
    )

    result = await repository.delete(location_id)

    assert result is True
    assert await repository.get_by_id(location_id) is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_returns_false_for_missing_location(
    test_database,
):
    repository = LocationRepository()

    result = await repository.delete(999)

    assert result is False


@pytest.mark.repository
@pytest.mark.asyncio
async def test_coordinates_are_saved_correctly(test_database):
    repository = LocationRepository()

    location_id = await repository.create(
        title="Филиал",
        address="Ташкент",
        latitude=41.311081,
        longitude=69.240562,
    )

    location = await repository.get_by_id(location_id)

    assert location is not None
    assert location["latitude"] == pytest.approx(41.311081)
    assert location["longitude"] == pytest.approx(69.240562)