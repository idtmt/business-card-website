import pytest
from httpx import AsyncClient


@pytest.mark.api
@pytest.mark.integration
@pytest.mark.parametrize(
    "payload",
    [
        {
            "title": "Основной филиал",
            "address": "Ташкент, ул. Навои, 10",
            "latitude": 41.3111,
            "longitude": 69.2797,
            "position": 0,
            "is_hidden": False,
        },
        {
            "title": "Скрытый филиал",
            "address": "Ташкент, ул. Амира Темура, 20",
            "latitude": 41.2995,
            "longitude": 69.2401,
            "position": 1,
            "is_hidden": True,
        },
    ],
)
async def test_create_location(
    client: AsyncClient,
    test_database,
    admin_credentials,
    payload: dict,
):
    response = await client.post(
        "/api/admin/locations",
        json=payload,
    )

    assert response.status_code == 201
    assert isinstance(response.json(), int)


@pytest.mark.api
@pytest.mark.integration
async def test_get_location(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    payload = {
        "title": "Основной филиал",
        "address": "Ташкент, ул. Навои, 10",
        "latitude": 41.3111,
        "longitude": 69.2797,
        "position": 0,
        "is_hidden": False,
    }

    create_response = await client.post(
        "/api/admin/locations",
        json=payload,
    )

    location_id = create_response.json()

    response = await client.get(
        f"/api/admin/locations/{location_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == location_id
    assert data["title"] == payload["title"]
    assert data["address"] == payload["address"]
    assert data["latitude"] == payload["latitude"]
    assert data["longitude"] == payload["longitude"]
    assert data["position"] == payload["position"]
    assert data["is_hidden"] == payload["is_hidden"]


@pytest.mark.api
@pytest.mark.integration
async def test_get_locations(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    locations = [
        {
            "title": "Первый филиал",
            "address": "Адрес 1",
            "latitude": 41.3111,
            "longitude": 69.2797,
            "position": 0,
            "is_hidden": False,
        },
        {
            "title": "Второй филиал",
            "address": "Адрес 2",
            "latitude": 41.3121,
            "longitude": 69.2807,
            "position": 1,
            "is_hidden": True,
        },
    ]

    for payload in locations:
        response = await client.post(
            "/api/admin/locations",
            json=payload,
        )
        assert response.status_code == 201

    response = await client.get(
        "/api/admin/locations",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Первый филиал"
    assert data[1]["title"] == "Второй филиал"


@pytest.mark.api
@pytest.mark.integration
async def test_get_locations_by_visibility(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    visible_location = {
        "title": "Видимый филиал",
        "address": "Адрес 1",
        "latitude": 41.3111,
        "longitude": 69.2797,
        "position": 0,
        "is_hidden": False,
    }

    hidden_location = {
        "title": "Скрытый филиал",
        "address": "Адрес 2",
        "latitude": 41.3121,
        "longitude": 69.2807,
        "position": 1,
        "is_hidden": True,
    }

    await client.post(
        "/api/admin/locations",
        json=visible_location,
    )

    await client.post(
        "/api/admin/locations",
        json=hidden_location,
    )

    response = await client.get(
        "/api/admin/locations",
        params={"is_hidden": False},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Видимый филиал"
    assert data[0]["is_hidden"] is False

    response = await client.get(
        "/api/admin/locations",
        params={"is_hidden": True},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Скрытый филиал"
    assert data[0]["is_hidden"] is True


@pytest.mark.api
@pytest.mark.integration
async def test_update_location(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    create_response = await client.post(
        "/api/admin/locations",
        json={
            "title": "Старый филиал",
            "address": "Старый адрес",
            "latitude": 41.3111,
            "longitude": 69.2797,
            "position": 0,
            "is_hidden": False,
        },
    )

    location_id = create_response.json()

    update_payload = {
        "title": "Новый филиал",
        "address": "Новый адрес",
        "latitude": 41.3200,
        "longitude": 69.2900,
        "position": 5,
        "is_hidden": True,
    }

    response = await client.put(
        f"/api/admin/locations/{location_id}",
        json=update_payload,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Локация обновлена.",
    }

    response = await client.get(
        f"/api/admin/locations/{location_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Новый филиал"
    assert data["address"] == "Новый адрес"
    assert data["latitude"] == 41.3200
    assert data["longitude"] == 69.2900
    assert data["position"] == 5
    assert data["is_hidden"] is True


@pytest.mark.api
@pytest.mark.integration
async def test_update_location_not_found(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    response = await client.put(
        "/api/admin/locations/999999",
        json={
            "title": "Филиал",
            "address": "Адрес",
            "latitude": 41.3111,
            "longitude": 69.2797,
            "position": 0,
            "is_hidden": False,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Локация не найдена."


@pytest.mark.api
@pytest.mark.integration
async def test_get_location_not_found(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    response = await client.get(
        "/api/admin/locations/999999",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Локация не найдена."


@pytest.mark.api
@pytest.mark.integration
async def test_delete_location(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    create_response = await client.post(
        "/api/admin/locations",
        json={
            "title": "Филиал для удаления",
            "address": "Адрес",
            "latitude": 41.3111,
            "longitude": 69.2797,
            "position": 0,
            "is_hidden": False,
        },
    )

    location_id = create_response.json()

    response = await client.delete(
        f"/api/admin/locations/{location_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Локация удалена.",
    }

    response = await client.get(
        f"/api/admin/locations/{location_id}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Локация не найдена."


@pytest.mark.api
@pytest.mark.integration
async def test_delete_location_not_found(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    response = await client.delete(
        "/api/admin/locations/999999",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Локация не найдена."


@pytest.mark.api
@pytest.mark.integration
async def test_create_location_validation_error(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    response = await client.post(
        "/api/admin/locations",
        json={
            "title": "",
            "address": "",
            "latitude": 100,
            "longitude": 200,
            "position": -1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 422