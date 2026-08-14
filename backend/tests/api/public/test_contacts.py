import pytest

from backend.repositories.contact_repository import ContactRepository


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_contacts_returns_visible_only(
    client,
    test_database,
) -> None:
    repository = ContactRepository()

    await repository.create(
        title="Telegram",
        value="@test",
        url="https://t.me/test",
        position=0,
        is_hidden=False,
    )

    await repository.create(
        title="Phone",
        value="+998901234567",
        position=1,
        is_hidden=True,
    )

    response = await client.get(
        "/api/contacts",
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Telegram",
            "value": "@test",
            "url": "https://t.me/test",
            "icon": None,
            "position": 0,
            "is_hidden": False,
        },
    ]


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_contacts_returns_empty_list_when_no_contacts(
    client,
    test_database,
) -> None:
    response = await client.get(
        "/api/contacts",
    )

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_contact_success(
    client,
    test_database,
) -> None:
    repository = ContactRepository()

    contact_id = await repository.create(
        title="Telegram",
        value="@test",
        url="https://t.me/test",
        icon="telegram",
        position=0,
        is_hidden=False,
    )

    response = await client.get(
        f"/api/contacts/{contact_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": contact_id,
        "title": "Telegram",
        "value": "@test",
        "url": "https://t.me/test",
        "icon": "telegram",
        "position": 0,
        "is_hidden": False,
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_hidden_contact_returns_not_found(
    client,
    test_database,
) -> None:
    repository = ContactRepository()

    contact_id = await repository.create(
        title="Phone",
        value="+998901234567",
        position=0,
        is_hidden=True,
    )

    response = await client.get(
        f"/api/contacts/{contact_id}",
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Контакт не найден.",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_nonexistent_contact_returns_not_found(
    client,
    test_database,
) -> None:
    response = await client.get(
        "/api/contacts/999",
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Контакт не найден.",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_contact_rejects_invalid_id(
    client,
    test_database,
) -> None:
    response = await client.get(
        "/api/contacts/invalid",
    )

    assert response.status_code == 422