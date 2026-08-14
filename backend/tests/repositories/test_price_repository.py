import pytest

from backend.repositories.price_repository import PriceRepository
from backend.repositories.service_repository import ServiceRepository


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_returns_id(test_database):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    price_id = await price_repository.create(
        service_id=service_id,
        title="Короткие волосы",
        price="50 000 сум",
    )

    assert price_id == 1


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_saves_all_fields(test_database):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    price_id = await price_repository.create(
        service_id=service_id,
        title="Мужская стрижка",
        price="80 000 сум",
        position=3,
        is_hidden=True,
    )

    price = await price_repository.get_by_id(price_id)

    assert price == {
        "id": price_id,
        "service_id": service_id,
        "title": "Мужская стрижка",
        "price": "80 000 сум",
        "position": 3,
        "is_hidden": 1,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_id_returns_existing_price(test_database):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Окрашивание",
    )

    price_id = await price_repository.create(
        service_id=service_id,
        title="Окрашивание волос",
        price="250 000 сум",
    )

    result = await price_repository.get_by_id(price_id)

    assert result == {
        "id": price_id,
        "service_id": service_id,
        "title": "Окрашивание волос",
        "price": "250 000 сум",
        "position": 0,
        "is_hidden": 0,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_missing_price(
    test_database,
):
    repository = PriceRepository()

    result = await repository.get_by_id(999)

    assert result is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_service_returns_prices_in_position_order(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    first_id = await price_repository.create(
        service_id=service_id,
        title="Второй вариант",
        price="70 000 сум",
        position=2,
    )

    second_id = await price_repository.create(
        service_id=service_id,
        title="Первый вариант",
        price="50 000 сум",
        position=1,
    )

    prices = await price_repository.get_by_service(
        service_id,
    )

    assert [price["id"] for price in prices] == [
        second_id,
        first_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_service_uses_id_as_secondary_sort(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    first_id = await price_repository.create(
        service_id=service_id,
        title="Первый",
        price="50 000 сум",
        position=1,
    )

    second_id = await price_repository.create(
        service_id=service_id,
        title="Второй",
        price="60 000 сум",
        position=1,
    )

    prices = await price_repository.get_by_service(
        service_id,
    )

    assert [price["id"] for price in prices] == [
        first_id,
        second_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_service_returns_empty_list_when_no_prices(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    result = await price_repository.get_by_service(
        service_id,
    )

    assert result == []


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_service_filters_visible_prices(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    visible_id = await price_repository.create(
        service_id=service_id,
        title="Видимая цена",
        price="50 000 сум",
        is_hidden=False,
    )

    await price_repository.create(
        service_id=service_id,
        title="Скрытая цена",
        price="60 000 сум",
        is_hidden=True,
    )

    prices = await price_repository.get_by_service(
        service_id,
        is_hidden=False,
    )

    assert [price["id"] for price in prices] == [
        visible_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_service_returns_only_hidden_prices(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    await price_repository.create(
        service_id=service_id,
        title="Видимая цена",
        price="50 000 сум",
        is_hidden=False,
    )

    hidden_id = await price_repository.create(
        service_id=service_id,
        title="Скрытая цена",
        price="60 000 сум",
        is_hidden=True,
    )

    prices = await price_repository.get_by_service(
        service_id,
        is_hidden=True,
    )

    assert [price["id"] for price in prices] == [
        hidden_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_returns_prices_grouped_by_service(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    first_service_id = await service_repository.create(
        name="Стрижка",
    )

    second_service_id = await service_repository.create(
        name="Окрашивание",
    )

    first_price_id = await price_repository.create(
        service_id=first_service_id,
        title="Стрижка",
        price="50 000 сум",
        position=1,
    )

    second_price_id = await price_repository.create(
        service_id=second_service_id,
        title="Окрашивание",
        price="200 000 сум",
        position=1,
    )

    prices = await price_repository.get_all()

    assert [price["id"] for price in prices] == [
        first_price_id,
        second_price_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_filters_hidden_prices(test_database):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    visible_id = await price_repository.create(
        service_id=service_id,
        title="Видимая",
        price="50 000 сум",
        is_hidden=False,
    )

    await price_repository.create(
        service_id=service_id,
        title="Скрытая",
        price="60 000 сум",
        is_hidden=True,
    )

    prices = await price_repository.get_all(
        is_hidden=False,
    )

    assert [price["id"] for price in prices] == [
        visible_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_updates_existing_price(test_database):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    price_id = await price_repository.create(
        service_id=service_id,
        title="Старая цена",
        price="50 000 сум",
    )

    result = await price_repository.update(
        price_id=price_id,
        title="Новая цена",
        price="80 000 сум",
        position=5,
        is_hidden=True,
    )

    assert result is True

    price = await price_repository.get_by_id(price_id)

    assert price == {
        "id": price_id,
        "service_id": service_id,
        "title": "Новая цена",
        "price": "80 000 сум",
        "position": 5,
        "is_hidden": 1,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_returns_false_for_missing_price(
    test_database,
):
    repository = PriceRepository()

    result = await repository.update(
        price_id=999,
        title="Цена",
        price="50 000 сум",
    )

    assert result is False


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_removes_existing_price(test_database):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    price_id = await price_repository.create(
        service_id=service_id,
        title="Удаляемая цена",
        price="50 000 сум",
    )

    result = await price_repository.delete(price_id)

    assert result is True
    assert await price_repository.get_by_id(price_id) is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_returns_false_for_missing_price(
    test_database,
):
    repository = PriceRepository()

    result = await repository.delete(999)

    assert result is False


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_service_cascades_to_prices(
    test_database,
):
    service_repository = ServiceRepository()
    price_repository = PriceRepository()

    service_id = await service_repository.create(
        name="Стрижка",
    )

    price_id = await price_repository.create(
        service_id=service_id,
        title="Цена",
        price="50 000 сум",
    )

    result = await service_repository.delete(service_id)

    assert result is True
    assert await price_repository.get_by_id(price_id) is None