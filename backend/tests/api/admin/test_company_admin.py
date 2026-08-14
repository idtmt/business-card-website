import pytest
import pytest_asyncio

from backend.repositories.company_repository import CompanyRepository


@pytest_asyncio.fixture(autouse=True)
async def authenticate_admin():
    pass


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_company_requires_authorization(
    client,
    test_database,
) -> None:
    response = await client.get(
        "/api/admin/company",
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Требуется авторизация.",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_create_company_requires_authorization(
    client,
    test_database,
) -> None:
    response = await client.post(
        "/api/admin/company",
        json={
            "name": "Test Company",
            "description": "Test description",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Требуется авторизация.",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_update_company_requires_authorization(
    client,
    test_database,
) -> None:
    response = await client.put(
        "/api/admin/company",
        json={
            "name": "Updated Company",
            "description": "Updated description",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Требуется авторизация.",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_company_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    repository = CompanyRepository()

    await repository.create(
        name="Test Company",
        description="Test description",
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
        "/api/admin/company",
    )

    assert response.status_code == 200
    assert response.json() == {
        "name": "Test Company",
        "description": "Test description",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_create_company_success(
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
        "/api/admin/company",
        json={
            "name": "Test Company",
            "description": "Test description",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Информация о компании создана.",
    }

    repository = CompanyRepository()

    company = await repository.get()

    assert company == {
        "id": 1,
        "name": "Test Company",
        "description": "Test description",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_update_company_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    repository = CompanyRepository()

    await repository.create(
        name="Old Company",
        description="Old description",
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
        "/api/admin/company",
        json={
            "name": "Updated Company",
            "description": "Updated description",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Информация о компании обновлена.",
    }

    company = await repository.get()

    assert company == {
        "id": 1,
        "name": "Updated Company",
        "description": "Updated description",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_create_company_rejects_empty_name(
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
        "/api/admin/company",
        json={
            "name": "",
            "description": "Test description",
        },
    )

    assert response.status_code == 422


@pytest.mark.api
@pytest.mark.asyncio
async def test_update_company_returns_not_found_when_company_does_not_exist(
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
        "/api/admin/company",
        json={
            "name": "Updated Company",
            "description": "Updated description",
        },
    )

    assert response.status_code == 404