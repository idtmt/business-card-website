import pytest
from httpx import AsyncClient

from backend.config import settings
from backend.database.connection import get_connection


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_locations_returns_only_visible_locations(
    client: AsyncClient,
    test_database,
):
    async with get_connection() as connection:
        await connection.execute(
            """
            INSERT INTO locations (
                title,
                address,
                latitude,
                longitude,
                position,
                is_hidden
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "Основной филиал",
                "Ташкент, ул. Амира Темура, 1",
                41.3111,
                69.2797,
                0,
                0,
            ),
        )

        await connection.execute(
            """
            INSERT INTO locations (
                title,
                address,
                latitude,
                longitude,
                position,
                is_hidden
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "Скрытый филиал",
                "Ташкент, ул. Навои, 10",
                41.2995,
                69.2401,
                1,
                1,
            ),
        )

        await connection.commit()

    response = await client.get("/api/locations")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Основной филиал"
    assert data[0]["address"] == "Ташкент, ул. Амира Темура, 1"
    assert data[0]["latitude"] == 41.3111
    assert data[0]["longitude"] == 69.2797
    assert data[0]["position"] == 0
    assert "is_hidden" not in data[0]
    assert data[0]["schedules"] == []


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_location_returns_location_with_schedules(
    client: AsyncClient,
    test_database,
):
    async with get_connection() as connection:
        cursor = await connection.execute(
            """
            INSERT INTO locations (
                title,
                address,
                latitude,
                longitude,
                position,
                is_hidden
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "Основной филиал",
                "Ташкент, ул. Амира Темура, 1",
                41.3111,
                69.2797,
                0,
                0,
            ),
        )

        location_id = cursor.lastrowid

        await connection.execute(
            """
            INSERT INTO schedules (
                location_id,
                weekday,
                start_time,
                end_time,
                is_day_off
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                location_id,
                0,
                "09:00",
                "18:00",
                0,
            ),
        )

        await connection.commit()

    response = await client.get(
        f"/api/locations/{location_id}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == location_id
    assert data["title"] == "Основной филиал"
    assert data["address"] == "Ташкент, ул. Амира Темура, 1"
    assert data["latitude"] == 41.3111
    assert data["longitude"] == 69.2797
    assert data["position"] == 0

    assert len(data["schedules"]) == 1

    schedule = data["schedules"][0]

    assert schedule["weekday"] == 0
    assert schedule["start_time"] == "09:00"
    assert schedule["end_time"] == "18:00"
    assert schedule["is_day_off"] is False


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_location_returns_404_for_hidden_location(
    client: AsyncClient,
    test_database,
):
    async with get_connection() as connection:
        cursor = await connection.execute(
            """
            INSERT INTO locations (
                title,
                address,
                latitude,
                longitude,
                position,
                is_hidden
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "Скрытый филиал",
                "Ташкент, ул. Навои, 10",
                41.2995,
                69.2401,
                0,
                1,
            ),
        )

        location_id = cursor.lastrowid

        await connection.commit()

    response = await client.get(
        f"/api/locations/{location_id}",
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Локация не найдена."
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_location_returns_404_for_nonexistent_location(
    client: AsyncClient,
    test_database,
):
    response = await client.get("/api/locations/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Локация не найдена."
    }