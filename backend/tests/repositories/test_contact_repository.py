import pytest

from backend.database.init_db import DatabaseInitializer
from backend.repositories.contact_repository import ContactRepository


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_returns_contact_id(test_database):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    contact_id = await repository.create(
        title="Телефон",
        value="+998901234567",
        url="tel:+998901234567",
        icon="phone",
        position=1,
        is_hidden=False,
    )

    assert contact_id == 1


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_stores_all_fields(test_database):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    contact_id = await repository.create(
        title="Telegram",
        value="@example",
        url="https://t.me/example",
        icon="telegram",
        position=5,
        is_hidden=True,
    )

    contact = await repository.get_by_id(contact_id)

    assert contact == {
        "id": contact_id,
        "title": "Telegram",
        "value": "@example",
        "url": "https://t.me/example",
        "icon": "telegram",
        "position": 5,
        "is_hidden": 1,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_with_optional_fields_as_none(test_database):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    contact_id = await repository.create(
        title="Телефон",
        value="+998901234567",
    )

    contact = await repository.get_by_id(contact_id)

    assert contact is not None
    assert contact["title"] == "Телефон"
    assert contact["value"] == "+998901234567"
    assert contact["url"] is None
    assert contact["icon"] is None
    assert contact["position"] == 0
    assert contact["is_hidden"] == 0


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_id_returns_contact(test_database):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    contact_id = await repository.create(
        title="Instagram",
        value="@example",
    )

    contact = await repository.get_by_id(contact_id)

    assert contact is not None
    assert contact["id"] == contact_id
    assert contact["title"] == "Instagram"
    assert contact["value"] == "@example"


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_nonexistent_contact(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    contact = await repository.get_by_id(999)

    assert contact is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_returns_empty_list_for_empty_table(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    contacts = await repository.get_all()

    assert contacts == []


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_returns_all_contacts(test_database):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    await repository.create(
        title="Телефон",
        value="+998901111111",
        position=1,
    )

    await repository.create(
        title="Telegram",
        value="@example",
        position=2,
    )

    contacts = await repository.get_all()

    assert len(contacts) == 2
    assert contacts[0]["title"] == "Телефон"
    assert contacts[1]["title"] == "Telegram"


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_orders_by_position_then_id(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    first_id = await repository.create(
        title="Первый",
        value="1",
        position=2,
    )

    second_id = await repository.create(
        title="Второй",
        value="2",
        position=1,
    )

    third_id = await repository.create(
        title="Третий",
        value="3",
        position=2,
    )

    contacts = await repository.get_all()

    assert [contact["id"] for contact in contacts] == [
        second_id,
        first_id,
        third_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_filters_hidden_contacts(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    await repository.create(
        title="Видимый",
        value="visible",
        is_hidden=False,
    )

    await repository.create(
        title="Скрытый",
        value="hidden",
        is_hidden=True,
    )

    contacts = await repository.get_all(is_hidden=True)

    assert len(contacts) == 1
    assert contacts[0]["title"] == "Скрытый"
    assert contacts[0]["is_hidden"] == 1


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_filters_visible_contacts(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    await repository.create(
        title="Видимый",
        value="visible",
        is_hidden=False,
    )

    await repository.create(
        title="Скрытый",
        value="hidden",
        is_hidden=True,
    )

    contacts = await repository.get_all(is_hidden=False)

    assert len(contacts) == 1
    assert contacts[0]["title"] == "Видимый"
    assert contacts[0]["is_hidden"] == 0


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_without_filter_returns_both_visible_and_hidden(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    await repository.create(
        title="Видимый",
        value="visible",
        is_hidden=False,
    )

    await repository.create(
        title="Скрытый",
        value="hidden",
        is_hidden=True,
    )

    contacts = await repository.get_all()

    assert len(contacts) == 2


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_returns_true_for_existing_contact(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    contact_id = await repository.create(
        title="Телефон",
        value="old",
    )

    result = await repository.update(
        contact_id=contact_id,
        title="Телефон",
        value="new",
        url="tel:+998901234567",
        icon="phone",
        position=10,
        is_hidden=True,
    )

    assert result is True


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_changes_all_fields(test_database):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    contact_id = await repository.create(
        title="Старое название",
        value="old",
        url="old-url",
        icon="old-icon",
        position=1,
        is_hidden=False,
    )

    await repository.update(
        contact_id=contact_id,
        title="Новое название",
        value="new",
        url="new-url",
        icon="new-icon",
        position=10,
        is_hidden=True,
    )

    contact = await repository.get_by_id(contact_id)

    assert contact == {
        "id": contact_id,
        "title": "Новое название",
        "value": "new",
        "url": "new-url",
        "icon": "new-icon",
        "position": 10,
        "is_hidden": 1,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_can_set_optional_fields_to_none(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    contact_id = await repository.create(
        title="Контакт",
        value="value",
        url="url",
        icon="icon",
    )

    result = await repository.update(
        contact_id=contact_id,
        title="Контакт",
        value="value",
        url=None,
        icon=None,
    )

    assert result is True

    contact = await repository.get_by_id(contact_id)

    assert contact["url"] is None
    assert contact["icon"] is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_returns_false_for_nonexistent_contact(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    result = await repository.update(
        contact_id=999,
        title="Контакт",
        value="value",
    )

    assert result is False


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_returns_true_for_existing_contact(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    contact_id = await repository.create(
        title="Телефон",
        value="+998901234567",
    )

    result = await repository.delete(contact_id)

    assert result is True


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_removes_contact(test_database):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    contact_id = await repository.create(
        title="Телефон",
        value="+998901234567",
    )

    await repository.delete(contact_id)

    contact = await repository.get_by_id(contact_id)

    assert contact is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_returns_false_for_nonexistent_contact(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = ContactRepository()

    result = await repository.delete(999)

    assert result is False