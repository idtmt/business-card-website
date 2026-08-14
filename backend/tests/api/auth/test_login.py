import pytest
from pwdlib import PasswordHash

from backend.config import settings


password_hash = PasswordHash.recommended()


@pytest.fixture
def admin_credentials(monkeypatch):
    username = "admin"
    password = "admin_password"

    monkeypatch.setattr(
        settings,
        "admin_username",
        username,
    )

    monkeypatch.setattr(
        settings,
        "admin_password_hash",
        password_hash.hash(password),
    )

    return username, password


@pytest.mark.api
@pytest.mark.asyncio
async def test_login_success(
    client,
    admin_credentials,
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
    assert response.json() == {
        "message": "Авторизация выполнена успешно.",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_login_sets_access_token_cookie(
    client,
    admin_credentials,
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

    set_cookie = response.headers["set-cookie"]

    assert "access_token=" in set_cookie
    assert "HttpOnly" in set_cookie
    assert "Path=/" in set_cookie


@pytest.mark.api
@pytest.mark.asyncio
async def test_login_rejects_wrong_username(
    client,
    admin_credentials,
) -> None:
    _, password = admin_credentials

    response = await client.post(
        "/api/auth/login",
        json={
            "username": "wrong_username",
            "password": password,
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Неверный логин или пароль.",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_login_rejects_wrong_password(
    client,
    admin_credentials,
) -> None:
    username, _ = admin_credentials

    response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": "wrong_password",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Неверный логин или пароль.",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_login_rejects_empty_username(
    client,
    admin_credentials,
) -> None:
    _, password = admin_credentials

    response = await client.post(
        "/api/auth/login",
        json={
            "username": "",
            "password": password,
        },
    )

    assert response.status_code == 422


@pytest.mark.api
@pytest.mark.asyncio
async def test_login_rejects_empty_password(
    client,
    admin_credentials,
) -> None:
    username, _ = admin_credentials

    response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": "",
        },
    )

    assert response.status_code == 422


@pytest.mark.api
@pytest.mark.asyncio
async def test_logout_deletes_access_token_cookie(
    client,
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
    assert "access_token" in client.cookies

    logout_response = await client.post(
        "/api/auth/logout",
    )

    assert logout_response.status_code == 200
    assert logout_response.json() == {
        "message": "Выход выполнен успешно.",
    }

    set_cookie = logout_response.headers["set-cookie"]

    assert "access_token=" in set_cookie
    assert "Max-Age=0" in set_cookie