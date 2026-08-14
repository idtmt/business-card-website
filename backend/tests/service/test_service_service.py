import pytest

from backend.core.exceptions import NotFoundError, ValidationError
from backend.repositories.service_repository import ServiceRepository
from backend.services.service_service import ServiceService


@pytest.fixture
def service_service() -> ServiceService:
    return ServiceService(
        repository=ServiceRepository(),
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_service(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Стрижка",
        description="Мужская стрижка",
    )

    assert service_id > 0

    service = await service_service.get_by_id(
        service_id,
    )

    assert service == {
        "id": service_id,
        "name": "Стрижка",
        "description": "Мужская стрижка",
        "position": 0,
        "is_hidden": 0,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_service_without_description(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Стрижка",
    )

    service = await service_service.get_by_id(
        service_id,
    )

    assert service["description"] is None


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_service_normalizes_strings(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="  Стрижка  ",
        description="  Мужская стрижка  ",
    )

    service = await service_service.get_by_id(
        service_id,
    )

    assert service["name"] == "Стрижка"
    assert service["description"] == "Мужская стрижка"


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_service_normalizes_empty_description(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Стрижка",
        description="   ",
    )

    service = await service_service.get_by_id(
        service_id,
    )

    assert service["description"] is None


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_service_with_custom_position_and_visibility(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Окрашивание",
        description="Окрашивание волос",
        position=5,
        is_hidden=True,
    )

    service = await service_service.get_by_id(
        service_id,
    )

    assert service["position"] == 5
    assert service["is_hidden"] == 1


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
    ],
)
async def test_create_service_rejects_empty_name(
    service_service: ServiceService,
    test_database,
    name: str,
) -> None:
    with pytest.raises(ValidationError):
        await service_service.create(
            name=name,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_service_rejects_invalid_position(
    service_service: ServiceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await service_service.create(
            name="Стрижка",
            position=-1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_service_rejects_non_bool_visibility(
    service_service: ServiceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await service_service.create(
            name="Стрижка",
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_service_by_id(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Стрижка",
        description="Мужская стрижка",
    )

    service = await service_service.get_by_id(
        service_id,
    )

    assert service["id"] == service_id
    assert service["name"] == "Стрижка"
    assert service["description"] == "Мужская стрижка"


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_service_by_id_raises_not_found(
    service_service: ServiceService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Услуга не найдена",
    ):
        await service_service.get_by_id(999)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_service_by_id_rejects_invalid_id(
    service_service: ServiceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await service_service.get_by_id(0)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_services(
    service_service: ServiceService,
    test_database,
) -> None:
    first_id = await service_service.create(
        name="Первая",
        position=2,
    )

    second_id = await service_service.create(
        name="Вторая",
        position=1,
    )

    services = await service_service.get_all()

    assert [service["id"] for service in services] == [
        second_id,
        first_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_services_orders_by_position_and_id(
    service_service: ServiceService,
    test_database,
) -> None:
    first_id = await service_service.create(
        name="Первая",
        position=1,
    )

    second_id = await service_service.create(
        name="Вторая",
        position=1,
    )

    third_id = await service_service.create(
        name="Третья",
        position=0,
    )

    services = await service_service.get_all()

    assert [service["id"] for service in services] == [
        third_id,
        first_id,
        second_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_services_filters_visible(
    service_service: ServiceService,
    test_database,
) -> None:
    visible_id = await service_service.create(
        name="Видимая",
        is_hidden=False,
    )

    await service_service.create(
        name="Скрытая",
        is_hidden=True,
    )

    services = await service_service.get_all(
        is_hidden=False,
    )

    assert [service["id"] for service in services] == [
        visible_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_services_filters_hidden(
    service_service: ServiceService,
    test_database,
) -> None:
    await service_service.create(
        name="Видимая",
        is_hidden=False,
    )

    hidden_id = await service_service.create(
        name="Скрытая",
        is_hidden=True,
    )

    services = await service_service.get_all(
        is_hidden=True,
    )

    assert [service["id"] for service in services] == [
        hidden_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_services_rejects_invalid_visibility(
    service_service: ServiceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await service_service.get_all(
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_service(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Старое название",
        description="Старое описание",
    )

    await service_service.update(
        service_id=service_id,
        name="Новое название",
        description="Новое описание",
        position=3,
        is_hidden=True,
    )

    service = await service_service.get_by_id(
        service_id,
    )

    assert service == {
        "id": service_id,
        "name": "Новое название",
        "description": "Новое описание",
        "position": 3,
        "is_hidden": 1,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_service_normalizes_strings(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Старое",
    )

    await service_service.update(
        service_id=service_id,
        name="  Новое название  ",
        description="  Новое описание  ",
    )

    service = await service_service.get_by_id(
        service_id,
    )

    assert service["name"] == "Новое название"
    assert service["description"] == "Новое описание"


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_service_normalizes_empty_description(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Стрижка",
        description="Описание",
    )

    await service_service.update(
        service_id=service_id,
        name="Стрижка",
        description="   ",
    )

    service = await service_service.get_by_id(
        service_id,
    )

    assert service["description"] is None


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_service_raises_not_found(
    service_service: ServiceService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Услуга не найдена",
    ):
        await service_service.update(
            service_id=999,
            name="Стрижка",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_service_rejects_invalid_id(
    service_service: ServiceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await service_service.update(
            service_id=0,
            name="Стрижка",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_service_rejects_empty_name(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Стрижка",
    )

    with pytest.raises(ValidationError):
        await service_service.update(
            service_id=service_id,
            name="   ",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_service_rejects_invalid_position(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Стрижка",
    )

    with pytest.raises(ValidationError):
        await service_service.update(
            service_id=service_id,
            name="Стрижка",
            position=-1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_service_rejects_non_bool_visibility(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Стрижка",
    )

    with pytest.raises(ValidationError):
        await service_service.update(
            service_id=service_id,
            name="Стрижка",
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_service(
    service_service: ServiceService,
    test_database,
) -> None:
    service_id = await service_service.create(
        name="Стрижка",
    )

    await service_service.delete(
        service_id,
    )

    with pytest.raises(NotFoundError):
        await service_service.get_by_id(
            service_id,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_service_raises_not_found(
    service_service: ServiceService,
    test_database,
) -> None:
    with pytest.raises(
        NotFoundError,
        match="Услуга не найдена",
    ):
        await service_service.delete(999)


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_service_rejects_invalid_id(
    service_service: ServiceService,
    test_database,
) -> None:
    with pytest.raises(ValidationError):
        await service_service.delete(0)