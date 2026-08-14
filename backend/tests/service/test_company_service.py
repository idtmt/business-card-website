from unittest.mock import AsyncMock

import pytest

from backend.core.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    ValidationError,
)
from backend.repositories.company_repository import CompanyRepository
from backend.services.company_service import CompanyService


@pytest.fixture
def repository() -> AsyncMock:
    return AsyncMock(spec=CompanyRepository)


@pytest.fixture
def service(
    repository: AsyncMock,
) -> CompanyService:
    return CompanyService(repository)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_returns_company(
    service: CompanyService,
    repository: AsyncMock,
):
    company = {
        "id": 1,
        "name": "Моя компания",
        "description": "Описание",
    }

    repository.get.return_value = company

    result = await service.get()

    assert result == company
    repository.get.assert_awaited_once()


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_returns_none_when_company_not_found(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = None

    result = await service.get()

    assert result is None
    repository.get.assert_awaited_once()


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_creates_company(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = None

    await service.create(
        name="Моя компания",
        description="Описание компании",
    )

    repository.get.assert_awaited_once()

    repository.create.assert_awaited_once_with(
        name="Моя компания",
        description="Описание компании",
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_strips_name(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = None

    await service.create(
        name="  Моя компания  ",
    )

    repository.create.assert_awaited_once_with(
        name="Моя компания",
        description=None,
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_strips_description(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = None

    await service.create(
        name="Моя компания",
        description="  Описание компании  ",
    )

    repository.create.assert_awaited_once_with(
        name="Моя компания",
        description="Описание компании",
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_normalizes_empty_description(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = None

    await service.create(
        name="Моя компания",
        description="   ",
    )

    repository.create.assert_awaited_once_with(
        name="Моя компания",
        description=None,
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_raises_already_exists_error(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = {
        "id": 1,
        "name": "Моя компания",
        "description": None,
    }

    with pytest.raises(
        AlreadyExistsError,
        match="Информация о компании уже существует.",
    ):
        await service.create(
            name="Новая компания",
        )

    repository.create.assert_not_awaited()


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_empty_name(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = None

    with pytest.raises(
        ValidationError,
        match='Поле "name" не может быть пустым.',
    ):
        await service.create(
            name="   ",
        )

    repository.create.assert_not_awaited()


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_non_string_name(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = None

    with pytest.raises(
        ValidationError,
        match='Поле "name" должно быть строкой.',
    ):
        await service.create(
            name=123,
        )

    repository.create.assert_not_awaited()


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_invalid_description(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = None

    with pytest.raises(
        ValidationError,
        match="Необязательное значение должно быть строкой или None.",
    ):
        await service.create(
            name="Моя компания",
            description=123,
        )

    repository.create.assert_not_awaited()


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_updates_existing_company(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = {
        "id": 1,
        "name": "Старое название",
        "description": "Старое описание",
    }

    await service.update(
        name="Новое название",
        description="Новое описание",
    )

    repository.get.assert_awaited_once()

    repository.update.assert_awaited_once_with(
        name="Новое название",
        description="Новое описание",
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_strips_name(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = {
        "id": 1,
        "name": "Старое название",
        "description": None,
    }

    await service.update(
        name="  Новое название  ",
    )

    repository.update.assert_awaited_once_with(
        name="Новое название",
        description=None,
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_strips_description(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = {
        "id": 1,
        "name": "Компания",
        "description": "Старое описание",
    }

    await service.update(
        name="Компания",
        description="  Новое описание  ",
    )

    repository.update.assert_awaited_once_with(
        name="Компания",
        description="Новое описание",
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_normalizes_empty_description(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = {
        "id": 1,
        "name": "Компания",
        "description": "Описание",
    }

    await service.update(
        name="Компания",
        description="   ",
    )

    repository.update.assert_awaited_once_with(
        name="Компания",
        description=None,
    )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_raises_not_found_error(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = None

    with pytest.raises(
        NotFoundError,
        match="Информация о компании не найдена.",
    ):
        await service.update(
            name="Компания",
        )

    repository.update.assert_not_awaited()


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_empty_name(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = {
        "id": 1,
        "name": "Компания",
        "description": None,
    }

    with pytest.raises(
        ValidationError,
        match='Поле "name" не может быть пустым.',
    ):
        await service.update(
            name="   ",
        )

    repository.update.assert_not_awaited()


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_non_string_name(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = {
        "id": 1,
        "name": "Компания",
        "description": None,
    }

    with pytest.raises(
        ValidationError,
        match='Поле "name" должно быть строкой.',
    ):
        await service.update(
            name=123,
        )

    repository.update.assert_not_awaited()


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_invalid_description(
    service: CompanyService,
    repository: AsyncMock,
):
    repository.get.return_value = {
        "id": 1,
        "name": "Компания",
        "description": None,
    }

    with pytest.raises(
        ValidationError,
        match="Необязательное значение должно быть строкой или None.",
    ):
        await service.update(
            name="Компания",
            description=123,
        )

    repository.update.assert_not_awaited()