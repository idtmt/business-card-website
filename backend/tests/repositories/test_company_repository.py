import pytest
import pytest_asyncio

from backend.database.init_db import DatabaseInitializer
from backend.repositories.company_repository import CompanyRepository


@pytest_asyncio.fixture
async def repository(test_database):
    await DatabaseInitializer.initialize()

    return CompanyRepository()


# ============================================================
# get
# ============================================================


@pytest.mark.integration
@pytest.mark.repository
async def test_get_returns_none_when_company_does_not_exist(
    repository,
):
    result = await repository.get()

    assert result is None


@pytest.mark.integration
@pytest.mark.repository
async def test_get_returns_existing_company(
    repository,
):
    await repository.create(
        name="Test Company",
        description="Test description",
    )

    result = await repository.get()

    assert result == {
        "id": 1,
        "name": "Test Company",
        "description": "Test description",
    }


# ============================================================
# create
# ============================================================


@pytest.mark.integration
@pytest.mark.repository
async def test_create_creates_company(
    repository,
):
    await repository.create(
        name="Test Company",
        description="Test description",
    )

    result = await repository.get()

    assert result is not None
    assert result["id"] == 1
    assert result["name"] == "Test Company"
    assert result["description"] == "Test description"


@pytest.mark.integration
@pytest.mark.repository
async def test_create_allows_empty_description(
    repository,
):
    await repository.create(
        name="Test Company",
    )

    result = await repository.get()

    assert result is not None
    assert result["name"] == "Test Company"
    assert result["description"] is None


@pytest.mark.integration
@pytest.mark.repository
async def test_create_rejects_second_company(
    repository,
):
    await repository.create(
        name="First Company",
    )

    with pytest.raises(Exception):
        await repository.create(
            name="Second Company",
        )


# ============================================================
# update
# ============================================================


@pytest.mark.integration
@pytest.mark.repository
async def test_update_updates_existing_company(
    repository,
):
    await repository.create(
        name="Old Name",
        description="Old description",
    )

    result = await repository.update(
        name="New Name",
        description="New description",
    )

    assert result is True

    company = await repository.get()

    assert company == {
        "id": 1,
        "name": "New Name",
        "description": "New description",
    }


@pytest.mark.integration
@pytest.mark.repository
async def test_update_returns_false_when_company_does_not_exist(
    repository,
):
    result = await repository.update(
        name="New Name",
        description="New description",
    )

    assert result is False


@pytest.mark.integration
@pytest.mark.repository
async def test_update_allows_empty_description(
    repository,
):
    await repository.create(
        name="Test Company",
        description="Description",
    )

    result = await repository.update(
        name="Updated Company",
    )

    assert result is True

    company = await repository.get()

    assert company is not None
    assert company["name"] == "Updated Company"
    assert company["description"] is None