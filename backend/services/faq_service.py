from typing import Any

from backend.core.exceptions import NotFoundError
from backend.repositories.faq_repository import FaqRepository
from backend.utils.validators import (
    validate_id,
    validate_position,
    validate_required,
    validate_visibility,
)


class FaqService:
    def __init__(
        self,
        repository: FaqRepository,
    ) -> None:
        self.repository = repository

    async def create(
        self,
        question: str,
        answer: str,
        position: int = 0,
        is_hidden: bool = False,
    ) -> int:
        question = validate_required(
            question,
            "question",
        )

        answer = validate_required(
            answer,
            "answer",
        )

        position = validate_position(
            position,
        )

        is_hidden = validate_visibility(
            is_hidden,
        )

        return await self.repository.create(
            question=question,
            answer=answer,
            position=position,
            is_hidden=is_hidden,
        )

    async def get_by_id(
        self,
        faq_id: int,
    ) -> dict[str, Any]:
        faq_id = validate_id(
            faq_id,
            "faq_id",
        )

        faq = await self.repository.get_by_id(
            faq_id,
        )

        if faq is None:
            raise NotFoundError(
                "FAQ не найден."
            )

        return faq

    async def get_all(
        self,
        is_hidden: bool | None = None,
    ) -> list[dict[str, Any]]:
        if is_hidden is not None:
            is_hidden = validate_visibility(
                is_hidden,
            )

        return await self.repository.get_all(
            is_hidden=is_hidden,
        )

    async def update(
        self,
        faq_id: int,
        question: str,
        answer: str,
        position: int = 0,
        is_hidden: bool = False,
    ) -> None:
        faq_id = validate_id(
            faq_id,
            "faq_id",
        )

        question = validate_required(
            question,
            "question",
        )

        answer = validate_required(
            answer,
            "answer",
        )

        position = validate_position(
            position,
        )

        is_hidden = validate_visibility(
            is_hidden,
        )

        updated = await self.repository.update(
            faq_id=faq_id,
            question=question,
            answer=answer,
            position=position,
            is_hidden=is_hidden,
        )

        if not updated:
            raise NotFoundError(
                "FAQ не найден."
            )

    async def delete(
        self,
        faq_id: int,
    ) -> None:
        faq_id = validate_id(
            faq_id,
            "faq_id",
        )

        deleted = await self.repository.delete(
            faq_id,
        )

        if not deleted:
            raise NotFoundError(
                "FAQ не найден."
            )