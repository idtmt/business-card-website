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


async def create_service(
    client: AsyncClient,
) -> int:
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

    return response.json()


@pytest.mark.asyncio
async def test_create_price(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    service_id = await create_service(client)

    response = await client.post(
        "/api/admin/prices",
        json={
            "service_id": service_id,
            "title": "Короткая стрижка",
            "price": "100 000 сум",
            "position": 1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 201

    price_id = response.json()

    assert isinstance(price_id, int)
    assert price_id > 0


@pytest.mark.asyncio
async def test_get_price(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    service_id = await create_service(client)

    create_response = await client.post(
        "/api/admin/prices",
        json={
            "service_id": service_id,
            "title": "Короткая стрижка",
            "price": "100 000 сум",
            "position": 1,
            "is_hidden": False,
        },
    )

    price_id = create_response.json()

    response = await client.get(
        f"/api/admin/prices/{price_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == price_id
    assert data["service_id"] == service_id
    assert data["title"] == "Короткая стрижка"
    assert data["price"] == "100 000 сум"
    assert data["position"] == 1
    assert data["is_hidden"] is False


@pytest.mark.asyncio
async def test_get_prices_by_service(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    service_id = await create_service(client)

    await client.post(
        "/api/admin/prices",
        json={
            "service_id": service_id,
            "title": "Короткая стрижка",
            "price": "100 000 сум",
            "position": 1,
            "is_hidden": False,
        },
    )

    await client.post(
        "/api/admin/prices",
        json={
            "service_id": service_id,
            "title": "Длинная стрижка",
            "price": "150 000 сум",
            "position": 2,
            "is_hidden": False,
        },
    )

    response = await client.get(
        f"/api/admin/prices/service/{service_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Короткая стрижка"
    assert data[1]["title"] == "Длинная стрижка"


@pytest.mark.asyncio
async def test_get_prices_by_service_filter_by_visibility(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    service_id = await create_service(client)

    await client.post(
        "/api/admin/prices",
        json={
            "service_id": service_id,
            "title": "Видимая цена",
            "price": "100 000 сум",
            "position": 1,
            "is_hidden": False,
        },
    )

    await client.post(
        "/api/admin/prices",
        json={
            "service_id": service_id,
            "title": "Скрытая цена",
            "price": "200 000 сум",
            "position": 2,
            "is_hidden": True,
        },
    )

    response = await client.get(
        f"/api/admin/prices/service/{service_id}",
        params={"is_hidden": False},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Видимая цена"
    assert data[0]["is_hidden"] is False

    response = await client.get(
        f"/api/admin/prices/service/{service_id}",
        params={"is_hidden": True},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Скрытая цена"
    assert data[0]["is_hidden"] is True


@pytest.mark.asyncio
async def test_get_all_prices(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    service_id = await create_service(client)

    await client.post(
        "/api/admin/prices",
        json={
            "service_id": service_id,
            "title": "Цена 1",
            "price": "100 000 сум",
            "position": 1,
            "is_hidden": False,
        },
    )

    await client.post(
        "/api/admin/prices",
        json={
            "service_id": service_id,
            "title": "Цена 2",
            "price": "150 000 сум",
            "position": 2,
            "is_hidden": False,
        },
    )

    response = await client.get("/api/admin/prices")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Цена 1"
    assert data[1]["title"] == "Цена 2"


@pytest.mark.asyncio
async def test_update_price(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    service_id = await create_service(client)

    create_response = await client.post(
        "/api/admin/prices",
        json={
            "service_id": service_id,
            "title": "Короткая стрижка",
            "price": "100 000 сум",
            "position": 1,
            "is_hidden": False,
        },
    )

    price_id = create_response.json()

    response = await client.put(
        f"/api/admin/prices/{price_id}",
        json={
            "title": "Короткая стрижка — премиум",
            "price": "150 000 сум",
            "position": 5,
            "is_hidden": True,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Цена обновлена.",
    }

    response = await client.get(
        f"/api/admin/prices/{price_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Короткая стрижка — премиум"
    assert data["price"] == "150 000 сум"
    assert data["position"] == 5
    assert data["is_hidden"] is True


@pytest.mark.asyncio
async def test_delete_price(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    service_id = await create_service(client)

    create_response = await client.post(
        "/api/admin/prices",
        json={
            "service_id": service_id,
            "title": "Короткая стрижка",
            "price": "100 000 сум",
            "position": 1,
            "is_hidden": False,
        },
    )

    price_id = create_response.json()

    response = await client.delete(
        f"/api/admin/prices/{price_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Цена удалена.",
    }

    response = await client.get(
        f"/api/admin/prices/{price_id}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Цена не найдена."


@pytest.mark.asyncio
async def test_get_nonexistent_price(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    response = await client.get("/api/admin/prices/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Цена не найдена."


@pytest.mark.asyncio
async def test_update_nonexistent_price(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    response = await client.put(
        "/api/admin/prices/999999",
        json={
            "title": "Стрижка",
            "price": "100 000 сум",
            "position": 1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Цена не найдена."


@pytest.mark.asyncio
async def test_delete_nonexistent_price(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    response = await client.delete("/api/admin/prices/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Цена не найдена."


@pytest.mark.asyncio
async def test_create_price_for_nonexistent_service(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    response = await client.post(
        "/api/admin/prices",
        json={
            "service_id": 999999,
            "title": "Стрижка",
            "price": "100 000 сум",
            "position": 1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Услуга не найдена."


@pytest.mark.asyncio
async def test_create_price_validation_error(
    client: AsyncClient,
    test_database,
    admin_credentials: tuple[str, str],
):
    await login(client, admin_credentials)

    service_id = await create_service(client)

    response = await client.post(
        "/api/admin/prices",
        json={
            "service_id": service_id,
            "title": "",
            "price": "",
            "position": 1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 422