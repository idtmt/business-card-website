import pytest

from backend.core.exceptions import NotFoundError, ValidationError
from backend.repositories.contact_repository import ContactRepository
from backend.services.contact_service import ContactService


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_creates_contact(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await service.create(
        title="Телефон",
        value="+998901234567",
    )

    assert contact_id == 1


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_normalizes_fields(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await service.create(
        title="  Телефон  ",
        value="  +998901234567  ",
        url="  https://example.com  ",
        icon="  phone  ",
    )

    contact = await repository.get_by_id(contact_id)

    assert contact is not None
    assert contact["title"] == "Телефон"
    assert contact["value"] == "+998901234567"
    assert contact["url"] == "https://example.com"
    assert contact["icon"] == "phone"


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_normalizes_empty_optional_fields(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await service.create(
        title="Телефон",
        value="+998901234567",
        url="   ",
        icon="",
    )

    contact = await repository.get_by_id(contact_id)

    assert contact is not None
    assert contact["url"] is None
    assert contact["icon"] is None


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_saves_position_and_visibility(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await service.create(
        title="Telegram",
        value="@example",
        position=5,
        is_hidden=True,
    )

    contact = await repository.get_by_id(contact_id)

    assert contact is not None
    assert contact["position"] == 5
    assert contact["is_hidden"] == 1


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_empty_title(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            title="   ",
            value="123",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_non_string_title(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            title=123,
            value="123",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_empty_value(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            title="Телефон",
            value="   ",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_non_string_value(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            title="Телефон",
            value=123,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_invalid_url(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            title="Телефон",
            value="123",
            url=123,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_invalid_icon(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            title="Телефон",
            value="123",
            icon=123,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_negative_position(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            title="Телефон",
            value="123",
            position=-1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_invalid_position_type(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            title="Телефон",
            value="123",
            position="1",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_invalid_visibility(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            title="Телефон",
            value="123",
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_by_id_returns_existing_contact(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await repository.create(
        title="Телефон",
        value="+998901234567",
    )

    result = await service.get_by_id(contact_id)

    assert result == {
        "id": contact_id,
        "title": "Телефон",
        "value": "+998901234567",
        "url": None,
        "icon": None,
        "position": 0,
        "is_hidden": 0,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_by_id_raises_not_found_for_missing_contact(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(NotFoundError):
        await service.get_by_id(999)


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "contact_id",
    [0, -1, "1", True],
)
async def test_get_by_id_rejects_invalid_id(
    test_database,
    contact_id,
):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.get_by_id(contact_id)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_returns_contacts(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    first_id = await repository.create(
        title="Телефон",
        value="+998901234567",
    )

    second_id = await repository.create(
        title="Telegram",
        value="@example",
    )

    result = await service.get_all()

    assert [contact["id"] for contact in result] == [
        first_id,
        second_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_passes_visibility_filter(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    visible_id = await repository.create(
        title="Телефон",
        value="+998901234567",
        is_hidden=False,
    )

    await repository.create(
        title="Telegram",
        value="@hidden",
        is_hidden=True,
    )

    result = await service.get_all(is_hidden=False)

    assert [contact["id"] for contact in result] == [
        visible_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_returns_only_hidden_contacts(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    await repository.create(
        title="Телефон",
        value="+998901234567",
        is_hidden=False,
    )

    hidden_id = await repository.create(
        title="Telegram",
        value="@hidden",
        is_hidden=True,
    )

    result = await service.get_all(is_hidden=True)

    assert [contact["id"] for contact in result] == [
        hidden_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_rejects_invalid_visibility(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.get_all(is_hidden=1)


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_updates_existing_contact(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await repository.create(
        title="Старый контакт",
        value="old",
    )

    await service.update(
        contact_id=contact_id,
        title="Новый контакт",
        value="new",
        url="https://example.com",
        icon="telegram",
        position=5,
        is_hidden=True,
    )

    contact = await repository.get_by_id(contact_id)

    assert contact == {
        "id": contact_id,
        "title": "Новый контакт",
        "value": "new",
        "url": "https://example.com",
        "icon": "telegram",
        "position": 5,
        "is_hidden": 1,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_normalizes_fields(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await repository.create(
        title="Старое",
        value="old",
    )

    await service.update(
        contact_id=contact_id,
        title="  Новое  ",
        value="  new  ",
        url="  https://example.com  ",
        icon="  telegram  ",
    )

    contact = await repository.get_by_id(contact_id)

    assert contact is not None
    assert contact["title"] == "Новое"
    assert contact["value"] == "new"
    assert contact["url"] == "https://example.com"
    assert contact["icon"] == "telegram"


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_can_clear_optional_fields(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await repository.create(
        title="Контакт",
        value="123",
        url="https://example.com",
        icon="phone",
    )

    await service.update(
        contact_id=contact_id,
        title="Контакт",
        value="123",
        url="   ",
        icon="",
    )

    contact = await repository.get_by_id(contact_id)

    assert contact is not None
    assert contact["url"] is None
    assert contact["icon"] is None


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_raises_not_found_for_missing_contact(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(NotFoundError):
        await service.update(
            contact_id=999,
            title="Контакт",
            value="123",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_invalid_id(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.update(
            contact_id=0,
            title="Контакт",
            value="123",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_empty_title(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await repository.create(
        title="Контакт",
        value="123",
    )

    with pytest.raises(ValidationError):
        await service.update(
            contact_id=contact_id,
            title="   ",
            value="123",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_empty_value(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await repository.create(
        title="Контакт",
        value="123",
    )

    with pytest.raises(ValidationError):
        await service.update(
            contact_id=contact_id,
            title="Контакт",
            value="   ",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_invalid_position(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await repository.create(
        title="Контакт",
        value="123",
    )

    with pytest.raises(ValidationError):
        await service.update(
            contact_id=contact_id,
            title="Контакт",
            value="123",
            position=-1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_invalid_visibility(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await repository.create(
        title="Контакт",
        value="123",
    )

    with pytest.raises(ValidationError):
        await service.update(
            contact_id=contact_id,
            title="Контакт",
            value="123",
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_deletes_existing_contact(test_database):
    repository = ContactRepository()
    service = ContactService(repository)

    contact_id = await repository.create(
        title="Удаляемый контакт",
        value="123",
    )

    await service.delete(contact_id)

    assert await repository.get_by_id(contact_id) is None


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_raises_not_found_for_missing_contact(
    test_database,
):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(NotFoundError):
        await service.delete(999)


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "contact_id",
    [0, -1, "1", True],
)
async def test_delete_rejects_invalid_id(
    test_database,
    contact_id,
):
    repository = ContactRepository()
    service = ContactService(repository)

    with pytest.raises(ValidationError):
        await service.delete(contact_id)