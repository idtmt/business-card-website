import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.api


async def login(
    client: AsyncClient,
    admin_credentials: tuple[str, str],
) -> None:
    username, password = admin_credentials

    response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_service(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    response = await client.post(
        "/api/admin/services",
        json={
            "name": "Стрижка",
            "description": "Мужская стрижка",
            "position": 1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 201

    service_id = response.json()

    assert isinstance(service_id, int)
    assert service_id > 0


@pytest.mark.asyncio
async def test_get_service(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    create_response = await client.post(
        "/api/admin/services",
        json={
            "name": "Стрижка",
            "description": "Мужская стрижка",
            "position": 1,
            "is_hidden": False,
        },
    )

    service_id = create_response.json()

    response = await client.get(
        f"/api/admin/services/{service_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == service_id
    assert data["name"] == "Стрижка"
    assert data["description"] == "Мужская стрижка"
    assert data["position"] == 1
    assert data["is_hidden"] is False


@pytest.mark.asyncio
async def test_get_services(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    await client.post(
        "/api/admin/services",
        json={
            "name": "Стрижка",
            "description": "Описание",
            "position": 1,
            "is_hidden": False,
        },
    )

    await client.post(
        "/api/admin/services",
        json={
            "name": "Окрашивание",
            "description": None,
            "position": 2,
            "is_hidden": False,
        },
    )

    response = await client.get("/api/admin/services")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Стрижка"
    assert data[1]["name"] == "Окрашивание"


@pytest.mark.asyncio
async def test_get_services_filter_by_visibility(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    await client.post(
        "/api/admin/services",
        json={
            "name": "Видимая услуга",
            "description": None,
            "position": 1,
            "is_hidden": False,
        },
    )

    await client.post(
        "/api/admin/services",
        json={
            "name": "Скрытая услуга",
            "description": None,
            "position": 2,
            "is_hidden": True,
        },
    )

    response = await client.get(
        "/api/admin/services",
        params={"is_hidden": False},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Видимая услуга"
    assert data[0]["is_hidden"] is False

    response = await client.get(
        "/api/admin/services",
        params={"is_hidden": True},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Скрытая услуга"
    assert data[0]["is_hidden"] is True


@pytest.mark.asyncio
async def test_update_service(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    create_response = await client.post(
        "/api/admin/services",
        json={
            "name": "Стрижка",
            "description": "Старое описание",
            "position": 1,
            "is_hidden": False,
        },
    )

    service_id = create_response.json()

    response = await client.put(
        f"/api/admin/services/{service_id}",
        json={
            "name": "Мужская стрижка",
            "description": "Новое описание",
            "position": 5,
            "is_hidden": True,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Услуга обновлена.",
    }

    response = await client.get(
        f"/api/admin/services/{service_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Мужская стрижка"
    assert data["description"] == "Новое описание"
    assert data["position"] == 5
    assert data["is_hidden"] is True


@pytest.mark.asyncio
async def test_delete_service(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    create_response = await client.post(
        "/api/admin/services",
        json={
            "name": "Стрижка",
            "description": None,
            "position": 1,
            "is_hidden": False,
        },
    )

    service_id = create_response.json()

    response = await client.delete(
        f"/api/admin/services/{service_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Услуга удалена.",
    }

    response = await client.get(
        f"/api/admin/services/{service_id}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Услуга не найдена."


@pytest.mark.asyncio
async def test_get_nonexistent_service(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    response = await client.get("/api/admin/services/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Услуга не найдена."


@pytest.mark.asyncio
async def test_update_nonexistent_service(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    response = await client.put(
        "/api/admin/services/999999",
        json={
            "name": "Стрижка",
            "description": None,
            "position": 1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Услуга не найдена."


@pytest.mark.asyncio
async def test_delete_nonexistent_service(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    response = await client.delete("/api/admin/services/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Услуга не найдена."


@pytest.mark.asyncio
async def test_create_service_validation_error(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    response = await client.post(
        "/api/admin/services",
        json={
            "name": "",
            "description": None,
            "position": 1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 422