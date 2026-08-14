from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pwdlib import PasswordHash

from backend.config import settings
from backend.database.init_db import DatabaseInitializer
from backend.main import app


@pytest.fixture
def admin_credentials() -> tuple[str, str]:
    username = "admin"
    password = "admin_password"

    settings.admin_username = username
    settings.admin_password_hash = PasswordHash.recommended().hash(
        password,
    )

    return username, password


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture(autouse=True)
async def authenticate_admin(
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


@pytest_asyncio.fixture
async def test_database(
    tmp_path: Path,
    monkeypatch,
):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        settings,
        "database_path",
        str(database_path),
    )

    await DatabaseInitializer.initialize()

    yield database_path