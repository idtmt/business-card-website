from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import HTTPException

from backend.config import settings
from backend.core.security import (
    create_access_token,
    decode_access_token,
    verify_password,
)


@pytest.mark.unit
def test_verify_password_accepts_correct_password() -> None:
    password = "StrongPassword123!"

    from pwdlib import PasswordHash

    password_hash = PasswordHash.recommended()
    hashed_password = password_hash.hash(password)

    assert verify_password(
        password,
        hashed_password,
    ) is True


@pytest.mark.unit
def test_verify_password_rejects_incorrect_password() -> None:
    password = "StrongPassword123!"
    wrong_password = "WrongPassword123!"

    from pwdlib import PasswordHash

    password_hash = PasswordHash.recommended()
    hashed_password = password_hash.hash(password)

    assert verify_password(
        wrong_password,
        hashed_password,
    ) is False


@pytest.mark.unit
def test_create_access_token_contains_admin_username() -> None:
    token = create_access_token()

    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=["HS256"],
    )

    assert payload["sub"] == settings.admin_username


@pytest.mark.unit
def test_create_access_token_contains_expiration() -> None:
    token = create_access_token()

    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=["HS256"],
    )

    assert "exp" in payload
    assert payload["exp"] > datetime.now(timezone.utc).timestamp()


@pytest.mark.unit
def test_decode_access_token_returns_username() -> None:
    token = create_access_token()

    username = decode_access_token(token)

    assert username == settings.admin_username


@pytest.mark.unit
def test_decode_access_token_rejects_invalid_token() -> None:
    with pytest.raises(
        HTTPException,
        match="Недействительная авторизация",
    ) as exc_info:
        decode_access_token("invalid-token")

    assert exc_info.value.status_code == 401


@pytest.mark.unit
def test_decode_access_token_rejects_token_with_wrong_secret() -> None:
    wrong_secret = "wrong-secret-key-that-is-at-least-32-bytes-long"

    token = jwt.encode(
        {
            "sub": settings.admin_username,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=60),
        },
        wrong_secret,
        algorithm="HS256",
    )

    with pytest.raises(
        HTTPException,
        match="Недействительная авторизация",
    ) as exc_info:
        decode_access_token(token)

    assert exc_info.value.status_code == 401


@pytest.mark.unit
def test_decode_access_token_rejects_wrong_username() -> None:
    token = jwt.encode(
        {
            "sub": "another-user",
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=60),
        },
        settings.secret_key,
        algorithm="HS256",
    )

    with pytest.raises(
        HTTPException,
        match="Недействительная авторизация",
    ) as exc_info:
        decode_access_token(token)

    assert exc_info.value.status_code == 401


@pytest.mark.unit
def test_decode_access_token_rejects_expired_token() -> None:
    token = jwt.encode(
        {
            "sub": settings.admin_username,
            "exp": datetime.now(timezone.utc)
            - timedelta(minutes=1),
        },
        settings.secret_key,
        algorithm="HS256",
    )

    with pytest.raises(
        HTTPException,
        match="Недействительная авторизация",
    ) as exc_info:
        decode_access_token(token)

    assert exc_info.value.status_code == 401


@pytest.mark.unit
def test_decode_access_token_rejects_token_without_username() -> None:
    token = jwt.encode(
        {
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=60),
        },
        settings.secret_key,
        algorithm="HS256",
    )

    with pytest.raises(
        HTTPException,
        match="Недействительная авторизация",
    ) as exc_info:
        decode_access_token(token)

    assert exc_info.value.status_code == 401