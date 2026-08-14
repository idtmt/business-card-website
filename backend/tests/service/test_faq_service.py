import pytest

from backend.core.exceptions import NotFoundError, ValidationError
from backend.repositories.faq_repository import FaqRepository
from backend.services.faq_service import FaqService


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_creates_faq(test_database):
    repository = FaqRepository()
    service = FaqService(repository)

    faq_id = await service.create(
        question="Как записаться?",
        answer="Через Telegram.",
    )

    assert faq_id == 1


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_normalizes_question_and_answer(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    faq_id = await service.create(
        question="  Как записаться?  ",
        answer="  Через Telegram.  ",
    )

    faq = await repository.get_by_id(faq_id)

    assert faq is not None
    assert faq["question"] == "Как записаться?"
    assert faq["answer"] == "Через Telegram."


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_saves_position_and_visibility(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    faq_id = await service.create(
        question="Вопрос",
        answer="Ответ",
        position=5,
        is_hidden=True,
    )

    faq = await repository.get_by_id(faq_id)

    assert faq is not None
    assert faq["position"] == 5
    assert faq["is_hidden"] == 1


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_empty_question(test_database):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            question="   ",
            answer="Ответ",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_non_string_question(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            question=123,
            answer="Ответ",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_empty_answer(test_database):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            question="Вопрос",
            answer="   ",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_non_string_answer(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            question="Вопрос",
            answer=123,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_negative_position(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            question="Вопрос",
            answer="Ответ",
            position=-1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_invalid_position_type(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            question="Вопрос",
            answer="Ответ",
            position="1",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_create_rejects_invalid_visibility(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(ValidationError):
        await service.create(
            question="Вопрос",
            answer="Ответ",
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_by_id_returns_existing_faq(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    faq_id = await repository.create(
        question="Как записаться?",
        answer="Через Telegram.",
    )

    result = await service.get_by_id(faq_id)

    assert result == {
        "id": faq_id,
        "question": "Как записаться?",
        "answer": "Через Telegram.",
        "position": 0,
        "is_hidden": 0,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_by_id_raises_not_found_for_missing_faq(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(NotFoundError):
        await service.get_by_id(999)


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "faq_id",
    [0, -1, "1", True],
)
async def test_get_by_id_rejects_invalid_id(
    test_database,
    faq_id,
):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(ValidationError):
        await service.get_by_id(faq_id)


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_returns_faqs(test_database):
    repository = FaqRepository()
    service = FaqService(repository)

    first_id = await repository.create(
        question="Первый вопрос",
        answer="Первый ответ",
    )

    second_id = await repository.create(
        question="Второй вопрос",
        answer="Второй ответ",
    )

    result = await service.get_all()

    assert [faq["id"] for faq in result] == [
        first_id,
        second_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_passes_visibility_filter(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    visible_id = await repository.create(
        question="Видимый вопрос",
        answer="Ответ",
        is_hidden=False,
    )

    await repository.create(
        question="Скрытый вопрос",
        answer="Ответ",
        is_hidden=True,
    )

    result = await service.get_all(is_hidden=False)

    assert [faq["id"] for faq in result] == [
        visible_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_returns_only_hidden_faqs(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    await repository.create(
        question="Видимый вопрос",
        answer="Ответ",
        is_hidden=False,
    )

    hidden_id = await repository.create(
        question="Скрытый вопрос",
        answer="Ответ",
        is_hidden=True,
    )

    result = await service.get_all(is_hidden=True)

    assert [faq["id"] for faq in result] == [
        hidden_id,
    ]


@pytest.mark.service
@pytest.mark.asyncio
async def test_get_all_rejects_invalid_visibility(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(ValidationError):
        await service.get_all(is_hidden=1)


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_updates_existing_faq(test_database):
    repository = FaqRepository()
    service = FaqService(repository)

    faq_id = await repository.create(
        question="Старый вопрос",
        answer="Старый ответ",
    )

    await service.update(
        faq_id=faq_id,
        question="Новый вопрос",
        answer="Новый ответ",
        position=5,
        is_hidden=True,
    )

    faq = await repository.get_by_id(faq_id)

    assert faq == {
        "id": faq_id,
        "question": "Новый вопрос",
        "answer": "Новый ответ",
        "position": 5,
        "is_hidden": 1,
    }


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_normalizes_question_and_answer(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    faq_id = await repository.create(
        question="Старый вопрос",
        answer="Старый ответ",
    )

    await service.update(
        faq_id=faq_id,
        question="  Новый вопрос  ",
        answer="  Новый ответ  ",
    )

    faq = await repository.get_by_id(faq_id)

    assert faq is not None
    assert faq["question"] == "Новый вопрос"
    assert faq["answer"] == "Новый ответ"


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_raises_not_found_for_missing_faq(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(NotFoundError):
        await service.update(
            faq_id=999,
            question="Вопрос",
            answer="Ответ",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_invalid_id(test_database):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(ValidationError):
        await service.update(
            faq_id=0,
            question="Вопрос",
            answer="Ответ",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_empty_question(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    faq_id = await repository.create(
        question="Вопрос",
        answer="Ответ",
    )

    with pytest.raises(ValidationError):
        await service.update(
            faq_id=faq_id,
            question="   ",
            answer="Ответ",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_empty_answer(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    faq_id = await repository.create(
        question="Вопрос",
        answer="Ответ",
    )

    with pytest.raises(ValidationError):
        await service.update(
            faq_id=faq_id,
            question="Вопрос",
            answer="   ",
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_invalid_position(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    faq_id = await repository.create(
        question="Вопрос",
        answer="Ответ",
    )

    with pytest.raises(ValidationError):
        await service.update(
            faq_id=faq_id,
            question="Вопрос",
            answer="Ответ",
            position=-1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_update_rejects_invalid_visibility(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    faq_id = await repository.create(
        question="Вопрос",
        answer="Ответ",
    )

    with pytest.raises(ValidationError):
        await service.update(
            faq_id=faq_id,
            question="Вопрос",
            answer="Ответ",
            is_hidden=1,
        )


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_deletes_existing_faq(test_database):
    repository = FaqRepository()
    service = FaqService(repository)

    faq_id = await repository.create(
        question="Удаляемый вопрос",
        answer="Ответ",
    )

    await service.delete(faq_id)

    assert await repository.get_by_id(faq_id) is None


@pytest.mark.service
@pytest.mark.asyncio
async def test_delete_raises_not_found_for_missing_faq(
    test_database,
):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(NotFoundError):
        await service.delete(999)


@pytest.mark.service
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "faq_id",
    [0, -1, "1", True],
)
async def test_delete_rejects_invalid_id(
    test_database,
    faq_id,
):
    repository = FaqRepository()
    service = FaqService(repository)

    with pytest.raises(ValidationError):
        await service.delete(faq_id)