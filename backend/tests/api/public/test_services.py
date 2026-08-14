import pytest

from backend.core.exceptions import NotFoundError
from backend.repositories.location_repository import LocationRepository
from backend.repositories.price_repository import PriceRepository
from backend.repositories.schedule_repository import ScheduleRepository
from backend.repositories.service_repository import ServiceRepository
from backend.services.public_location_service import PublicLocationService
from backend.services.public_service_service import PublicServiceService


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.asyncio
async def test_public_service_get_by_id(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
        description="Мужская стрижка",
        position=1,
        is_hidden=False,
    )

    await price_repository.create(
        service_id=service_id,
        title="Стандарт",
        price="100 000 сум",
        position=1,
        is_hidden=False,
    )

    service = PublicServiceService(
        service_repository=service_repository,
        price_repository=price_repository,
    )

    result = await service.get_by_id(service_id)

    assert result["id"] == service_id
    assert result["name"] == "Стрижка"
    assert result["description"] == "Мужская стрижка"
    assert result["prices"] == [
        {
            "id": result["prices"][0]["id"],
            "service_id": service_id,
            "title": "Стандарт",
            "price": "100 000 сум",
            "position": 1,
        }
    ]
    assert "is_hidden" not in result
    assert "is_hidden" not in result["prices"][0]


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.asyncio
async def test_public_service_get_by_id_excludes_hidden_prices(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    await price_repository.create(
        service_id=service_id,
        title="Открытая цена",
        price="100 000 сум",
        position=1,
        is_hidden=False,
    )

    await price_repository.create(
        service_id=service_id,
        title="Скрытая цена",
        price="200 000 сум",
        position=2,
        is_hidden=True,
    )

    service = PublicServiceService(
        service_repository=service_repository,
        price_repository=price_repository,
    )

    result = await service.get_by_id(service_id)

    assert len(result["prices"]) == 1
    assert result["prices"][0]["title"] == "Открытая цена"


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.asyncio
async def test_public_service_get_by_id_hidden_service(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Скрытая услуга",
        is_hidden=True,
    )

    service = PublicServiceService(
        service_repository=service_repository,
        price_repository=price_repository,
    )

    with pytest.raises(NotFoundError):
        await service.get_by_id(service_id)


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.asyncio
async def test_public_service_get_by_id_not_found(
    test_database,
):
    service = PublicServiceService(
        service_repository=ServiceRepository(),
        price_repository=PriceRepository(),
    )

    with pytest.raises(NotFoundError):
        await service.get_by_id(999999)


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.asyncio
async def test_public_service_get_all(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    visible_service_id = await service_repository.create(
        name="Стрижка",
        position=1,
        is_hidden=False,
    )

    await service_repository.create(
        name="Скрытая услуга",
        position=2,
        is_hidden=True,
    )

    await price_repository.create(
        service_id=visible_service_id,
        title="Мужская",
        price="100 000 сум",
        position=1,
        is_hidden=False,
    )

    service = PublicServiceService(
        service_repository=service_repository,
        price_repository=price_repository,
    )

    result = await service.get_all()

    assert len(result) == 1
    assert result[0]["name"] == "Стрижка"
    assert len(result[0]["prices"]) == 1
    assert result[0]["prices"][0]["title"] == "Мужская"


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.asyncio
async def test_public_service_get_all_orders_services_and_prices(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    first_id = await service_repository.create(
        name="Первая",
        position=2,
    )

    second_id = await service_repository.create(
        name="Вторая",
        position=1,
    )

    await price_repository.create(
        service_id=first_id,
        title="Цена 2",
        price="200",
        position=2,
    )

    await price_repository.create(
        service_id=first_id,
        title="Цена 1",
        price="100",
        position=1,
    )

    service = PublicServiceService(
        service_repository=service_repository,
        price_repository=price_repository,
    )

    result = await service.get_all()

    assert [item["id"] for item in result] == [
        second_id,
        first_id,
    ]

    assert [
        item["title"]
        for item in result[1]["prices"]
    ] == [
        "Цена 1",
        "Цена 2",
    ]


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.asyncio
async def test_public_location_get_by_id(
    test_database,
):
    location_repository = LocationRepository()
    schedule_repository = ScheduleRepository()

    location_id = await location_repository.create(
        title="Главный филиал",
        address="ул. Амира Темура, 10",
        latitude=41.3111,
        longitude=69.2797,
        position=1,
        is_hidden=False,
    )

    await schedule_repository.create(
        location_id=location_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
        is_day_off=False,
    )

    service = PublicLocationService(
        location_repository=location_repository,
        schedule_repository=schedule_repository,
    )

    result = await service.get_by_id(location_id)

    assert result["id"] == location_id
    assert result["title"] == "Главный филиал"
    assert result["address"] == "ул. Амира Темура, 10"
    assert result["latitude"] == 41.3111
    assert result["longitude"] == 69.2797
    assert len(result["schedules"]) == 1

    assert result["schedules"][0]["weekday"] == 0
    assert result["schedules"][0]["start_time"] == "09:00"
    assert result["schedules"][0]["end_time"] == "18:00"
    assert result["schedules"][0]["is_day_off"] == 0


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.asyncio
async def test_public_location_get_by_id_hidden_location(
    test_database,
):
    location_repository = LocationRepository()
    schedule_repository = ScheduleRepository()

    location_id = await location_repository.create(
        title="Скрытый филиал",
        address="Адрес",
        latitude=41.0,
        longitude=69.0,
        is_hidden=True,
    )

    service = PublicLocationService(
        location_repository=location_repository,
        schedule_repository=schedule_repository,
    )

    with pytest.raises(NotFoundError):
        await service.get_by_id(location_id)


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.asyncio
async def test_public_location_get_by_id_not_found(
    test_database,
):
    service = PublicLocationService(
        location_repository=LocationRepository(),
        schedule_repository=ScheduleRepository(),
    )

    with pytest.raises(NotFoundError):
        await service.get_by_id(999999)


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.asyncio
async def test_public_location_get_all(
    test_database,
):
    location_repository = LocationRepository()
    schedule_repository = ScheduleRepository()

    first_id = await location_repository.create(
        title="Первый филиал",
        address="Первый адрес",
        latitude=41.1,
        longitude=69.1,
        position=1,
    )

    await location_repository.create(
        title="Скрытый филиал",
        address="Скрытый адрес",
        latitude=41.2,
        longitude=69.2,
        position=2,
        is_hidden=True,
    )

    await schedule_repository.create(
        location_id=first_id,
        weekday=0,
        start_time="09:00",
        end_time="18:00",
    )

    service = PublicLocationService(
        location_repository=location_repository,
        schedule_repository=schedule_repository,
    )

    result = await service.get_all()

    assert len(result) == 1
    assert result[0]["id"] == first_id
    assert result[0]["title"] == "Первый филиал"
    assert len(result[0]["schedules"]) == 1


@pytest.mark.service
@pytest.mark.unit
@pytest.mark.asyncio
async def test_public_location_get_all_returns_locations_in_position_order(
    test_database,
):
    location_repository = LocationRepository()
    schedule_repository = ScheduleRepository()

    first_id = await location_repository.create(
        title="Первый",
        address="Адрес 1",
        latitude=41.0,
        longitude=69.0,
        position=2,
    )

    second_id = await location_repository.create(
        title="Второй",
        address="Адрес 2",
        latitude=41.1,
        longitude=69.1,
        position=1,
    )

    service = PublicLocationService(
        location_repository=location_repository,
        schedule_repository=schedule_repository,
    )

    result = await service.get_all()

    assert [item["id"] for item in result] == [
        second_id,
        first_id,
    ]