import pytest

from backend.core.exceptions import NotFoundError, ValidationError
from backend.repositories.price_repository import PriceRepository
from backend.repositories.service_repository import ServiceRepository
from backend.services.price_service import PriceService
from backend.services.service_service import ServiceService


@pytest.fixture
def price_service() -> PriceService:
    return PriceService(
        repository=PriceRepository(),
        service_repository=ServiceRepository(),
    )


async def create_service() -> int:
    service_service = ServiceService(
        repository=ServiceRepository(),
    )

    return await service_service.create(
        name="Стрижка",
        description="Мужская стрижка",
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_price(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    price_id = await price_service.create(
        service_id=service_id,
        title="Мужская стрижка",
        price="100 000 сум",
    )

    assert price_id > 0

    price = await price_service.get_by_id(
        price_id,
    )

    assert price == {
        "id": price_id,
        "service_id": service_id,
        "title": "Мужская стрижка",
        "price": "100 000 сум",
        "position": 0,
        "is_hidden": 0,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_price_with_custom_position_and_visibility(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    price_id = await price_service.create(
        service_id=service_id,
        title="Премиум стрижка",
        price="200 000 сум",
        position=5,
        is_hidden=True,
    )

    price = await price_service.get_by_id(
        price_id,
    )

    assert price["position"] == 5
    assert price["is_hidden"] == 1


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_price_normalizes_strings(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    price_id = await price_service.create(
        service_id=service_id,
        title="  Мужская стрижка  ",
        price="  100 000 сум  ",
    )

    price = await price_service.get_by_id(
        price_id,
    )

    assert price["title"] == "Мужская стрижка"
    assert price["price"] == "100 000 сум"


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "title",
    [
        "",
        "   ",
    ],
)
async def test_create_price_rejects_empty_title(
    price_service: PriceService,
    test_database,
    title: str,
) -> None:
    service_id = await create_service()

    with pytest.raises(ValidationError):
        await price_service.create(
            service_id=service_id,
            title=title,
            price="100 000 сум",
        )


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "price",
    [
        "",
        "   ",
    ],
)
async def test_create_price_rejects_empty_price(
    price_service: PriceService,
    test_database,
    price: str,
) -> None:
    service_id = await create_service()

    with pytest.raises(ValidationError):
        await price_service.create(
            service_id=service_id,
            title="Стрижка",
            price=price,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_price_rejects_invalid_service_id(
    price_service: PriceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await price_service.create(
            service_id=0,
            title="Стрижка",
            price="100 000 сум",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_price_raises_not_found_for_missing_service(
    price_service: PriceService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Услуга не найдена",
    ):
        await price_service.create(
            service_id=999,
            title="Стрижка",
            price="100 000 сум",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_price_rejects_invalid_position(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    with pytest.raises(ValidationError):
        await price_service.create(
            service_id=service_id,
            title="Стрижка",
            price="100 000 сум",
            position=-1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_price_rejects_non_bool_visibility(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    with pytest.raises(ValidationError):
        await price_service.create(
            service_id=service_id,
            title="Стрижка",
            price="100 000 сум",
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_price_by_id(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    price_id = await price_service.create(
        service_id=service_id,
        title="Стрижка",
        price="100 000 сум",
    )

    price = await price_service.get_by_id(
        price_id,
    )

    assert price["id"] == price_id
    assert price["service_id"] == service_id
    assert price["title"] == "Стрижка"
    assert price["price"] == "100 000 сум"


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_price_by_id_raises_not_found(
    price_service: PriceService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Цена не найдена",
    ):
        await price_service.get_by_id(999)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_price_by_id_rejects_invalid_id(
    price_service: PriceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await price_service.get_by_id(0)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_prices_by_service(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    first_id = await price_service.create(
        service_id=service_id,
        title="Стрижка",
        price="100 000 сум",
        position=1,
    )

    second_id = await price_service.create(
        service_id=service_id,
        title="Борода",
        price="50 000 сум",
        position=2,
    )

    prices = await price_service.get_by_service(
        service_id,
    )

    assert [price["id"] for price in prices] == [
        first_id,
        second_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_prices_by_service_orders_by_position_and_id(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    first_id = await price_service.create(
        service_id=service_id,
        title="Первая",
        price="100 000 сум",
        position=1,
    )

    second_id = await price_service.create(
        service_id=service_id,
        title="Вторая",
        price="200 000 сум",
        position=1,
    )

    third_id = await price_service.create(
        service_id=service_id,
        title="Третья",
        price="300 000 сум",
        position=0,
    )

    prices = await price_service.get_by_service(
        service_id,
    )

    assert [price["id"] for price in prices] == [
        third_id,
        first_id,
        second_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_prices_by_service_filters_visible(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    visible_id = await price_service.create(
        service_id=service_id,
        title="Видимая",
        price="100 000 сум",
        is_hidden=False,
    )

    await price_service.create(
        service_id=service_id,
        title="Скрытая",
        price="200 000 сум",
        is_hidden=True,
    )

    prices = await price_service.get_by_service(
        service_id=service_id,
        is_hidden=False,
    )

    assert [price["id"] for price in prices] == [
        visible_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_prices_by_service_filters_hidden(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    await price_service.create(
        service_id=service_id,
        title="Видимая",
        price="100 000 сум",
        is_hidden=False,
    )

    hidden_id = await price_service.create(
        service_id=service_id,
        title="Скрытая",
        price="200 000 сум",
        is_hidden=True,
    )

    prices = await price_service.get_by_service(
        service_id=service_id,
        is_hidden=True,
    )

    assert [price["id"] for price in prices] == [
        hidden_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_prices_by_service_raises_not_found_for_missing_service(
    price_service: PriceService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Услуга не найдена",
    ):
        await price_service.get_by_service(999)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_prices_by_service_rejects_invalid_service_id(
    price_service: PriceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await price_service.get_by_service(0)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_prices_by_service_rejects_invalid_visibility(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    with pytest.raises(ValidationError):
        await price_service.get_by_service(
            service_id=service_id,
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_prices(
    price_service: PriceService,
    test_database,
) -> None:
    first_service_id = await create_service()

    service_service = ServiceService(
        repository=ServiceRepository(),
    )

    second_service_id = await service_service.create(
        name="Окрашивание",
    )

    first_price_id = await price_service.create(
        service_id=first_service_id,
        title="Стрижка",
        price="100 000 сум",
    )

    second_price_id = await price_service.create(
        service_id=second_service_id,
        title="Окрашивание",
        price="300 000 сум",
    )

    prices = await price_service.get_all()

    assert [price["id"] for price in prices] == [
        first_price_id,
        second_price_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_prices_filters_visible(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    visible_id = await price_service.create(
        service_id=service_id,
        title="Видимая",
        price="100 000 сум",
        is_hidden=False,
    )

    await price_service.create(
        service_id=service_id,
        title="Скрытая",
        price="200 000 сум",
        is_hidden=True,
    )

    prices = await price_service.get_all(
        is_hidden=False,
    )

    assert [price["id"] for price in prices] == [
        visible_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_prices_filters_hidden(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    await price_service.create(
        service_id=service_id,
        title="Видимая",
        price="100 000 сум",
        is_hidden=False,
    )

    hidden_id = await price_service.create(
        service_id=service_id,
        title="Скрытая",
        price="200 000 сум",
        is_hidden=True,
    )

    prices = await price_service.get_all(
        is_hidden=True,
    )

    assert [price["id"] for price in prices] == [
        hidden_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_prices_rejects_invalid_visibility(
    price_service: PriceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await price_service.get_all(
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_price(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    price_id = await price_service.create(
        service_id=service_id,
        title="Старая цена",
        price="100 000 сум",
    )

    await price_service.update(
        price_id=price_id,
        title="Новая цена",
        price="150 000 сум",
        position=3,
        is_hidden=True,
    )

    price = await price_service.get_by_id(
        price_id,
    )

    assert price == {
        "id": price_id,
        "service_id": service_id,
        "title": "Новая цена",
        "price": "150 000 сум",
        "position": 3,
        "is_hidden": 1,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_price_normalizes_strings(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    price_id = await price_service.create(
        service_id=service_id,
        title="Старая",
        price="100 000 сум",
    )

    await price_service.update(
        price_id=price_id,
        title="  Новая цена  ",
        price="  150 000 сум  ",
    )

    price = await price_service.get_by_id(
        price_id,
    )

    assert price["title"] == "Новая цена"
    assert price["price"] == "150 000 сум"


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_price_raises_not_found(
    price_service: PriceService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Цена не найдена",
    ):
        await price_service.update(
            price_id=999,
            title="Стрижка",
            price="100 000 сум",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_price_rejects_invalid_id(
    price_service: PriceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await price_service.update(
            price_id=0,
            title="Стрижка",
            price="100 000 сум",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_price_rejects_empty_title(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    price_id = await price_service.create(
        service_id=service_id,
        title="Стрижка",
        price="100 000 сум",
    )

    with pytest.raises(ValidationError):
        await price_service.update(
            price_id=price_id,
            title="   ",
            price="100 000 сум",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_price_rejects_empty_price(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    price_id = await price_service.create(
        service_id=service_id,
        title="Стрижка",
        price="100 000 сум",
    )

    with pytest.raises(ValidationError):
        await price_service.update(
            price_id=price_id,
            title="Стрижка",
            price="   ",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_price_rejects_invalid_position(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    price_id = await price_service.create(
        service_id=service_id,
        title="Стрижка",
        price="100 000 сум",
    )

    with pytest.raises(ValidationError):
        await price_service.update(
            price_id=price_id,
            title="Стрижка",
            price="100 000 сум",
            position=-1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_price_rejects_non_bool_visibility(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    price_id = await price_service.create(
        service_id=service_id,
        title="Стрижка",
        price="100 000 сум",
    )

    with pytest.raises(ValidationError):
        await price_service.update(
            price_id=price_id,
            title="Стрижка",
            price="100 000 сум",
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_price(
    price_service: PriceService,
    test_database,
) -> None:
    service_id = await create_service()

    price_id = await price_service.create(
        service_id=service_id,
        title="Стрижка",
        price="100 000 сум",
    )

    await price_service.delete(
        price_id,
    )

    with pytest.raises(
        NotFoundError,
        match="Цена не найдена",
    ):
        await price_service.get_by_id(
            price_id,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_price_raises_not_found(
    price_service: PriceService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Цена не найдена",
    ):
        await price_service.delete(999)


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_price_rejects_invalid_id(
    price_service: PriceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await price_service.delete(0)