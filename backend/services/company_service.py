from typing import Any

from backend.core.exceptions import AlreadyExistsError, NotFoundError
from backend.repositories.company_repository import CompanyRepository
from backend.utils.validators import (
    normalize_optional,
    validate_required,
)


class CompanyService:
    def __init__(
        self,
        repository: CompanyRepository,
    ) -> None:
        self.repository = repository

    async def get(self) -> dict[str, Any] | None:
        return await self.repository.get()

    async def create(
        self,
        name: str,
        description: str | None = None,
    ) -> None:
        existing = await self.repository.get()

        if existing is not None:
            raise AlreadyExistsError(
                "Информация о компании уже существует."
            )

        name = validate_required(
            name,
            "name",
        )

        description = normalize_optional(description)

        await self.repository.create(
            name=name,
            description=description,
        )

    async def update(
        self,
        name: str,
        description: str | None = None,
    ) -> None:
        existing = await self.repository.get()

        if existing is None:
            raise NotFoundError(
                "Информация о компании не найдена."
            )

        name = validate_required(
            name,
            "name",
        )

        description = normalize_optional(description)

        await self.repository.update(
            name=name,
            description=description,
        )