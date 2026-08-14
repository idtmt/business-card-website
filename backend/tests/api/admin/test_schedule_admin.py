import pytest

from httpx import AsyncClient


async def create_test_location(
    client: AsyncClient,
) -> int:
    response = await client.post(
        "/api/admin/locations",
        json={
            "title": "Тестовый филиал",
            "address": "Тестовый адрес",
            "latitude": 41.3111,
            "longitude": 69.2797,
            "position": 0,
            "is_hidden": False,
        },
    )

    assert response.status_code == 201

    return response.json()


@pytest.mark.api
@pytest.mark.integration
async def test_create_schedule(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    location_id = await create_test_location(client)

    response = await client.post(
        "/api/admin/schedules",
        json={
            "location_id": location_id,
            "weekday": 1,
            "start_time": "09:00",
            "end_time": "18:00",
            "is_day_off": False,
        },
    )

    assert response.status_code == 201
    assert isinstance(response.json(), int)


@pytest.mark.api
@pytest.mark.integration
async def test_create_day_off_schedule(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    location_id = await create_test_location(client)

    response = await client.post(
        "/api/admin/schedules",
        json={
            "location_id": location_id,
            "weekday": 6,
            "start_time": None,
            "end_time": None,
            "is_day_off": True,
        },
    )

    assert response.status_code == 201
    assert isinstance(response.json(), int)


@pytest.mark.api
@pytest.mark.integration
async def test_get_schedule(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    location_id = await create_test_location(client)

    create_response = await client.post(
        "/api/admin/schedules",
        json={
            "location_id": location_id,
            "weekday": 1,
            "start_time": "09:00",
            "end_time": "18:00",
            "is_day_off": False,
        },
    )

    schedule_id = create_response.json()

    response = await client.get(
        f"/api/admin/schedules/{schedule_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == schedule_id
    assert data["location_id"] == location_id
    assert data["weekday"] == 1
    assert data["start_time"] == "09:00"
    assert data["end_time"] == "18:00"
    assert data["is_day_off"] is False


@pytest.mark.api
@pytest.mark.integration
async def test_get_schedule_by_location(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    location_id = await create_test_location(client)

    schedules = [
        {
            "location_id": location_id,
            "weekday": 1,
            "start_time": "09:00",
            "end_time": "18:00",
            "is_day_off": False,
        },
        {
            "location_id": location_id,
            "weekday": 2,
            "start_time": "10:00",
            "end_time": "19:00",
            "is_day_off": False,
        },
        {
            "location_id": location_id,
            "weekday": 6,
            "start_time": None,
            "end_time": None,
            "is_day_off": True,
        },
    ]

    for payload in schedules:
        response = await client.post(
            "/api/admin/schedules",
            json=payload,
        )

        assert response.status_code == 201

    response = await client.get(
        f"/api/admin/schedules/location/{location_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 3
    assert [schedule["weekday"] for schedule in data] == [1, 2, 6]


@pytest.mark.api
@pytest.mark.integration
async def test_get_schedule_by_location_and_weekday(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    location_id = await create_test_location(client)

    await client.post(
        "/api/admin/schedules",
        json={
            "location_id": location_id,
            "weekday": 3,
            "start_time": "09:30",
            "end_time": "18:30",
            "is_day_off": False,
        },
    )

    response = await client.get(
        f"/api/admin/schedules/location/{location_id}/weekday/3",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["location_id"] == location_id
    assert data["weekday"] == 3
    assert data["start_time"] == "09:30"
    assert data["end_time"] == "18:30"
    assert data["is_day_off"] is False


@pytest.mark.api
@pytest.mark.integration
async def test_get_schedule_not_found(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    response = await client.get(
        "/api/admin/schedules/999999",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Расписание не найдено."


@pytest.mark.api
@pytest.mark.integration
async def test_get_schedule_by_location_and_weekday_not_found(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    location_id = await create_test_location(client)

    response = await client.get(
        f"/api/admin/schedules/location/{location_id}/weekday/1",
    )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "Расписание для этого дня не найдено."
    )


@pytest.mark.api
@pytest.mark.integration
async def test_create_duplicate_schedule(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    location_id = await create_test_location(client)

    payload = {
        "location_id": location_id,
        "weekday": 1,
        "start_time": "09:00",
        "end_time": "18:00",
        "is_day_off": False,
    }

    response = await client.post(
        "/api/admin/schedules",
        json=payload,
    )

    assert response.status_code == 201

    response = await client.post(
        "/api/admin/schedules",
        json=payload,
    )

    assert response.status_code == 409
    assert (
        response.json()["detail"]
        == "Расписание для этого дня уже существует."
    )


@pytest.mark.api
@pytest.mark.integration
async def test_create_schedule_for_missing_location(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    response = await client.post(
        "/api/admin/schedules",
        json={
            "location_id": 999999,
            "weekday": 1,
            "start_time": "09:00",
            "end_time": "18:00",
            "is_day_off": False,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Локация не найдена."


@pytest.mark.api
@pytest.mark.integration
async def test_update_schedule(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    location_id = await create_test_location(client)

    create_response = await client.post(
        "/api/admin/schedules",
        json={
            "location_id": location_id,
            "weekday": 1,
            "start_time": "09:00",
            "end_time": "18:00",
            "is_day_off": False,
        },
    )

    schedule_id = create_response.json()

    response = await client.put(
        f"/api/admin/schedules/{schedule_id}",
        json={
            "weekday": 2,
            "start_time": "10:00",
            "end_time": "20:00",
            "is_day_off": False,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Расписание обновлено.",
    }

    response = await client.get(
        f"/api/admin/schedules/{schedule_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["weekday"] == 2
    assert data["start_time"] == "10:00"
    assert data["end_time"] == "20:00"
    assert data["is_day_off"] is False


@pytest.mark.api
@pytest.mark.integration
async def test_update_schedule_to_existing_weekday(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    location_id = await create_test_location(client)

    first_response = await client.post(
        "/api/admin/schedules",
        json={
            "location_id": location_id,
            "weekday": 1,
            "start_time": "09:00",
            "end_time": "18:00",
            "is_day_off": False,
        },
    )

    first_schedule_id = first_response.json()

    await client.post(
        "/api/admin/schedules",
        json={
            "location_id": location_id,
            "weekday": 2,
            "start_time": "10:00",
            "end_time": "19:00",
            "is_day_off": False,
        },
    )

    response = await client.put(
        f"/api/admin/schedules/{first_schedule_id}",
        json={
            "weekday": 2,
            "start_time": "09:00",
            "end_time": "18:00",
            "is_day_off": False,
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["detail"]
        == "Расписание для этого дня уже существует."
    )


@pytest.mark.api
@pytest.mark.integration
async def test_update_schedule_not_found(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    response = await client.put(
        "/api/admin/schedules/999999",
        json={
            "weekday": 1,
            "start_time": "09:00",
            "end_time": "18:00",
            "is_day_off": False,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Расписание не найдено."


@pytest.mark.api
@pytest.mark.integration
async def test_delete_schedule(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    location_id = await create_test_location(client)

    create_response = await client.post(
        "/api/admin/schedules",
        json={
            "location_id": location_id,
            "weekday": 1,
            "start_time": "09:00",
            "end_time": "18:00",
            "is_day_off": False,
        },
    )

    schedule_id = create_response.json()

    response = await client.delete(
        f"/api/admin/schedules/{schedule_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Расписание удалено.",
    }

    response = await client.get(
        f"/api/admin/schedules/{schedule_id}",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Расписание не найдено."


@pytest.mark.api
@pytest.mark.integration
async def test_delete_schedule_not_found(
    client: AsyncClient,
    test_database,
    admin_credentials,
):
    response = await client.delete(
        "/api/admin/schedules/999999",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Расписание не найдено."


@pytest.mark.api
@pytest.mark.integration
@pytest.mark.parametrize(
    "payload",
    [
        {
            "weekday": 1,
            "start_time": None,
            "end_time": "18:00",
            "is_day_off": False,
        },
        {
            "weekday": 1,
            "start_time": "09:00",
            "end_time": None,
            "is_day_off": False,
        },
        {
            "weekday": 1,
            "start_time": "18:00",
            "end_time": "09:00",
            "is_day_off": False,
        },
        {
            "weekday": 1,
            "start_time": "09:00",
            "end_time": "18:00",
            "is_day_off": True,
        },
    ],
)
async def test_create_schedule_invalid_times(
    client: AsyncClient,
    test_database,
    admin_credentials,
    payload: dict,
):
    location_id = await create_test_location(client)

    payload["location_id"] = location_id

    response = await client.post(
        "/api/admin/schedules",
        json=payload,
    )

    assert response.status_code == 422