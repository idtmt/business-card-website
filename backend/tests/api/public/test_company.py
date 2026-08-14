import pytest

from backend.repositories.company_repository import CompanyRepository


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_company_returns_company(
    client,
    test_database,
) -> None:
    repository = CompanyRepository()

    await repository.create(
        name="Test Company",
        description="Test description",
    )

    response = await client.get(
        "/api/company",
    )

    assert response.status_code == 200
    assert response.json() == {
        "name": "Test Company",
        "description": "Test description",
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_company_returns_null_when_company_does_not_exist(
    client,
    test_database,
) -> None:
    response = await client.get(
        "/api/company",
    )

    assert response.status_code == 200
    assert response.json() is None