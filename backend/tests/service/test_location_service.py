import pytest

from backend.core.exceptions import NotFoundError, ValidationError
from backend.repositories.location_repository import LocationRepository
from backend.services.location_service import LocationService


@pytest.fixture
def location_service() -> LocationService:
    return LocationService(
        repository=LocationRepository(),
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_location(
    location_service: LocationService,
    test_database,
) -> None:
    location_id = await location_service.create(
        title="Главный офис",
        address="ул. Амира Темура, 10",
        latitude=41.3111,
        longitude=69.2797,
    )

    assert location_id > 0

    location = await location_service.get_by_id(
        location_id,
    )

    assert location == {
        "id": location_id,
        "title": "Главный офис",
        "address": "ул. Амира Темура, 10",
        "latitude": 41.3111,
        "longitude": 69.2797,
        "position": 0,
        "is_hidden": 0,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_location_normalizes_required_strings(
    location_service: LocationService,
    test_database,
) -> None:
    location_id = await location_service.create(
        title="  Главный офис  ",
        address="  ул. Амира Темура, 10  ",
        latitude=41.3111,
        longitude=69.2797,
    )

    location = await location_service.get_by_id(
        location_id,
    )

    assert location["title"] == "Главный офис"
    assert location["address"] == "ул. Амира Темура, 10"


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_location_with_custom_position_and_visibility(
    location_service: LocationService,
    test_database,
) -> None:
    location_id = await location_service.create(
        title="Филиал",
        address="ул. Навои, 20",
        latitude=40.0000,
        longitude=70.0000,
        position=5,
        is_hidden=True,
    )

    location = await location_service.get_by_id(
        location_id,
    )

    assert location["position"] == 5
    assert location["is_hidden"] == 1


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "title,address",
    [
        ("", "Адрес"),
        ("   ", "Адрес"),
        ("Название", ""),
        ("Название", "   "),
    ],
)
async def test_create_location_rejects_empty_required_fields(
    location_service: LocationService,
    test_database,
    title: str,
    address: str,
) -> None:
    with pytest.raises(ValidationError):
        await location_service.create(
            title=title,
            address=address,
            latitude=41.3111,
            longitude=69.2797,
        )


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "latitude",
    [-90.1, 90.1],
)
async def test_create_location_rejects_invalid_latitude(
    location_service: LocationService,
    test_database,
    latitude: float,
) -> None:
    with pytest.raises(ValidationError):
        await location_service.create(
            title="Офис",
            address="Адрес",
            latitude=latitude,
            longitude=69.2797,
        )


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "longitude",
    [-180.1, 180.1],
)
async def test_create_location_rejects_invalid_longitude(
    location_service: LocationService,
    test_database,
    longitude: float,
) -> None:
    with pytest.raises(ValidationError):
        await location_service.create(
            title="Офис",
            address="Адрес",
            latitude=41.3111,
            longitude=longitude,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_location_accepts_boundary_coordinates(
    location_service: LocationService,
    test_database,
) -> None:
    location_id = await location_service.create(
        title="Офис",
        address="Адрес",
        latitude=90,
        longitude=180,
    )

    location = await location_service.get_by_id(
        location_id,
    )

    assert location["latitude"] == 90.0
    assert location["longitude"] == 180.0


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_location_rejects_invalid_position(
    location_service: LocationService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await location_service.create(
            title="Офис",
            address="Адрес",
            latitude=41.3111,
            longitude=69.2797,
            position=-1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_location_rejects_non_bool_visibility(
    location_service: LocationService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await location_service.create(
            title="Офис",
            address="Адрес",
            latitude=41.3111,
            longitude=69.2797,
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_location_by_id(
    location_service: LocationService,
    test_database,
) -> None:
    location_id = await location_service.create(
        title="Филиал",
        address="Адрес",
        latitude=41.3,
        longitude=69.2,
    )

    location = await location_service.get_by_id(
        location_id,
    )

    assert location["id"] == location_id
    assert location["title"] == "Филиал"


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_location_by_id_raises_not_found(
    location_service: LocationService,
    test_database,
) -> None:
    with pytest.raises(NotFoundError, match="Локация не найдена"):
        await location_service.get_by_id(999)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_location_by_id_rejects_invalid_id(
    location_service: LocationService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await location_service.get_by_id(0)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_locations(
    location_service: LocationService,
    test_database,
) -> None:
    first_id = await location_service.create(
        title="Первый",
        address="Адрес 1",
        latitude=41.3,
        longitude=69.2,
        position=2,
    )

    second_id = await location_service.create(
        title="Второй",
        address="Адрес 2",
        latitude=41.4,
        longitude=69.3,
        position=1,
    )

    locations = await location_service.get_all()

    assert [location["id"] for location in locations] == [
        second_id,
        first_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_locations_filters_by_visibility(
    location_service: LocationService,
    test_database,
) -> None:
    visible_id = await location_service.create(
        title="Видимая",
        address="Адрес 1",
        latitude=41.3,
        longitude=69.2,
        is_hidden=False,
    )

    hidden_id = await location_service.create(
        title="Скрытая",
        address="Адрес 2",
        latitude=41.4,
        longitude=69.3,
        is_hidden=True,
    )

    visible_locations = await location_service.get_all(
        is_hidden=False,
    )

    hidden_locations = await location_service.get_all(
        is_hidden=True,
    )

    assert [location["id"] for location in visible_locations] == [
        visible_id,
    ]

    assert [location["id"] for location in hidden_locations] == [
        hidden_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_location(
    location_service: LocationService,
    test_database,
) -> None:
    location_id = await location_service.create(
        title="Старое название",
        address="Старый адрес",
        latitude=41.3,
        longitude=69.2,
    )

    await location_service.update(
        location_id=location_id,
        title="Новое название",
        address="Новый адрес",
        latitude=42.0,
        longitude=70.0,
        position=3,
        is_hidden=True,
    )

    location = await location_service.get_by_id(
        location_id,
    )

    assert location == {
        "id": location_id,
        "title": "Новое название",
        "address": "Новый адрес",
        "latitude": 42.0,
        "longitude": 70.0,
        "position": 3,
        "is_hidden": 1,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_location_raises_not_found(
    location_service: LocationService,
    test_database,
) -> None:
    with pytest.raises(NotFoundError, match="Локация не найдена"):
        await location_service.update(
            location_id=999,
            title="Офис",
            address="Адрес",
            latitude=41.3,
            longitude=69.2,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_location(
    location_service: LocationService,
    test_database,
) -> None:
    location_id = await location_service.create(
        title="Офис",
        address="Адрес",
        latitude=41.3,
        longitude=69.2,
    )

    await location_service.delete(
        location_id,
    )

    with pytest.raises(NotFoundError):
        await location_service.get_by_id(
            location_id,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_location_raises_not_found(
    location_service: LocationService,
    test_database,
) -> None:
    with pytest.raises(NotFoundError, match="Локация не найдена"):
        await location_service.delete(999)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_locations_rejects_invalid_visibility(
    location_service: LocationService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await location_service.get_all(
            is_hidden=1,
        )