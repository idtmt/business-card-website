import pytest

from backend.repositories.service_repository import ServiceRepository


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_returns_id(test_database):
    repository = ServiceRepository()

    service_id = await repository.create(
        name="Стрижка",
        description="Мужская стрижка",
    )

    assert service_id == 1


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_saves_all_fields(test_database):
    repository = ServiceRepository()

    service_id = await repository.create(
        name="Стрижка",
        description="Мужская стрижка",
        position=3,
        is_hidden=True,
    )

    service = await repository.get_by_id(service_id)

    assert service == {
        "id": service_id,
        "name": "Стрижка",
        "description": "Мужская стрижка",
        "position": 3,
        "is_hidden": 1,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_allows_empty_description(test_database):
    repository = ServiceRepository()

    service_id = await repository.create(
        name="Стрижка",
    )

    service = await repository.get_by_id(service_id)

    assert service is not None
    assert service["name"] == "Стрижка"
    assert service["description"] is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_id_returns_existing_service(test_database):
    repository = ServiceRepository()

    service_id = await repository.create(
        name="Окрашивание",
        description="Окрашивание волос",
    )

    result = await repository.get_by_id(service_id)

    assert result == {
        "id": service_id,
        "name": "Окрашивание",
        "description": "Окрашивание волос",
        "position": 0,
        "is_hidden": 0,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_missing_service(
    test_database,
):
    repository = ServiceRepository()

    result = await repository.get_by_id(999)

    assert result is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_returns_services_in_position_order(
    test_database,
):
    repository = ServiceRepository()

    first_id = await repository.create(
        name="Второй",
        position=2,
    )

    second_id = await repository.create(
        name="Первый",
        position=1,
    )

    services = await repository.get_all()

    assert [service["id"] for service in services] == [
        second_id,
        first_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_uses_id_as_secondary_sort(
    test_database,
):
    repository = ServiceRepository()

    first_id = await repository.create(
        name="Первый",
        position=1,
    )

    second_id = await repository.create(
        name="Второй",
        position=1,
    )

    services = await repository.get_all()

    assert [service["id"] for service in services] == [
        first_id,
        second_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_returns_empty_list_when_no_services(
    test_database,
):
    repository = ServiceRepository()

    result = await repository.get_all()

    assert result == []


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_filters_visible_services(test_database):
    repository = ServiceRepository()

    visible_id = await repository.create(
        name="Видимая услуга",
        is_hidden=False,
    )

    await repository.create(
        name="Скрытая услуга",
        is_hidden=True,
    )

    services = await repository.get_all(is_hidden=False)

    assert [service["id"] for service in services] == [
        visible_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_returns_only_hidden_services(
    test_database,
):
    repository = ServiceRepository()

    await repository.create(
        name="Видимая услуга",
        is_hidden=False,
    )

    hidden_id = await repository.create(
        name="Скрытая услуга",
        is_hidden=True,
    )

    services = await repository.get_all(is_hidden=True)

    assert [service["id"] for service in services] == [
        hidden_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_updates_existing_service(test_database):
    repository = ServiceRepository()

    service_id = await repository.create(
        name="Старое название",
        description="Старое описание",
    )

    result = await repository.update(
        service_id=service_id,
        name="Новое название",
        description="Новое описание",
        position=5,
        is_hidden=True,
    )

    assert result is True

    service = await repository.get_by_id(service_id)

    assert service == {
        "id": service_id,
        "name": "Новое название",
        "description": "Новое описание",
        "position": 5,
        "is_hidden": 1,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_can_clear_description(test_database):
    repository = ServiceRepository()

    service_id = await repository.create(
        name="Услуга",
        description="Описание",
    )

    result = await repository.update(
        service_id=service_id,
        name="Услуга",
        description=None,
    )

    assert result is True

    service = await repository.get_by_id(service_id)

    assert service is not None
    assert service["description"] is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_returns_false_for_missing_service(
    test_database,
):
    repository = ServiceRepository()

    result = await repository.update(
        service_id=999,
        name="Услуга",
    )

    assert result is False


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_removes_existing_service(test_database):
    repository = ServiceRepository()

    service_id = await repository.create(
        name="Удаляемая услуга",
    )

    result = await repository.delete(service_id)

    assert result is True
    assert await repository.get_by_id(service_id) is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_returns_false_for_missing_service(
    test_database,
):
    repository = ServiceRepository()

    result = await repository.delete(999)

    assert result is False