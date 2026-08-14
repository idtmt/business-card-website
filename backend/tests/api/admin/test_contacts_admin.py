import pytest

from backend.repositories.contact_repository import ContactRepository


@pytest.mark.api
@pytest.mark.asyncio
async def test_create_contact_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    username, password = admin_credentials

    login_response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    response = await client.post(
        "/api/admin/contacts",
        json={
            "title": "Telegram",
            "value": "@test",
            "url": "https://t.me/test",
            "icon": "telegram",
            "position": 1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 201
    assert response.json() == 1

    repository = ContactRepository()

    contact = await repository.get_by_id(1)

    assert contact == {
        "id": 1,
        "title": "Telegram",
        "value": "@test",
        "url": "https://t.me/test",
        "icon": "telegram",
        "position": 1,
        "is_hidden": False,
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_contacts_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    repository = ContactRepository()

    await repository.create(
        title="Telegram",
        value="@test",
        position=0,
        is_hidden=False,
    )

    await repository.create(
        title="Phone",
        value="+998901234567",
        position=1,
        is_hidden=True,
    )

    username, password = admin_credentials

    login_response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    response = await client.get(
        "/api/admin/contacts",
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Telegram",
            "value": "@test",
            "url": None,
            "icon": None,
            "position": 0,
            "is_hidden": False,
        },
        {
            "id": 2,
            "title": "Phone",
            "value": "+998901234567",
            "url": None,
            "icon": None,
            "position": 1,
            "is_hidden": True,
        },
    ]


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_hidden_contacts(
    client,
    test_database,
    admin_credentials,
) -> None:
    repository = ContactRepository()

    await repository.create(
        title="Telegram",
        value="@visible",
        is_hidden=False,
    )

    await repository.create(
        title="Phone",
        value="+998901234567",
        is_hidden=True,
    )

    username, password = admin_credentials

    login_response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    response = await client.get(
        "/api/admin/contacts?is_hidden=true",
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 2,
            "title": "Phone",
            "value": "+998901234567",
            "url": None,
            "icon": None,
            "position": 0,
            "is_hidden": True,
        },
    ]


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_visible_contacts(
    client,
    test_database,
    admin_credentials,
) -> None:
    repository = ContactRepository()

    await repository.create(
        title="Telegram",
        value="@visible",
        is_hidden=False,
    )

    await repository.create(
        title="Phone",
        value="+998901234567",
        is_hidden=True,
    )

    username, password = admin_credentials

    login_response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    response = await client.get(
        "/api/admin/contacts?is_hidden=false",
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Telegram",
            "value": "@visible",
            "url": None,
            "icon": None,
            "position": 0,
            "is_hidden": False,
        },
    ]


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_contact_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    repository = ContactRepository()

    contact_id = await repository.create(
        title="Telegram",
        value="@test",
        url="https://t.me/test",
        icon="telegram",
        position=1,
        is_hidden=False,
    )

    username, password = admin_credentials

    login_response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    response = await client.get(
        f"/api/admin/contacts/{contact_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": contact_id,
        "title": "Telegram",
        "value": "@test",
        "url": "https://t.me/test",
        "icon": "telegram",
        "position": 1,
        "is_hidden": False,
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_update_contact_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    repository = ContactRepository()

    contact_id = await repository.create(
        title="Old title",
        value="Old value",
        position=0,
        is_hidden=False,
    )

    username, password = admin_credentials

    login_response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    response = await client.put(
        f"/api/admin/contacts/{contact_id}",
        json={
            "title": "Updated title",
            "value": "Updated value",
            "url": "https://example.com",
            "icon": "link",
            "position": 2,
            "is_hidden": True,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Контакт обновлен.",
    }

    contact = await repository.get_by_id(contact_id)

    assert contact == {
        "id": contact_id,
        "title": "Updated title",
        "value": "Updated value",
        "url": "https://example.com",
        "icon": "link",
        "position": 2,
        "is_hidden": True,
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_delete_contact_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    repository = ContactRepository()

    contact_id = await repository.create(
        title="Telegram",
        value="@test",
    )

    username, password = admin_credentials

    login_response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    response = await client.delete(
        f"/api/admin/contacts/{contact_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Контакт удален.",
    }

    assert await repository.get_by_id(contact_id) is None


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_nonexistent_contact_returns_not_found(
    client,
    test_database,
    admin_credentials,
) -> None:
    username, password = admin_credentials

    login_response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    response = await client.get(
        "/api/admin/contacts/999",
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Контакт не найден.",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_update_nonexistent_contact_returns_not_found(
    client,
    test_database,
    admin_credentials,
) -> None:
    username, password = admin_credentials

    login_response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    response = await client.put(
        "/api/admin/contacts/999",
        json={
            "title": "Updated title",
            "value": "Updated value",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Контакт не найден.",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_delete_nonexistent_contact_returns_not_found(
    client,
    test_database,
    admin_credentials,
) -> None:
    username, password = admin_credentials

    login_response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    response = await client.delete(
        "/api/admin/contacts/999",
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Контакт не найден.",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_create_contact_rejects_empty_title(
    client,
    test_database,
    admin_credentials,
) -> None:
    username, password = admin_credentials

    login_response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    response = await client.post(
        "/api/admin/contacts",
        json={
            "title": "",
            "value": "Test value",
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": 'Поле "title" не может быть пустым.',
    }