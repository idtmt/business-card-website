import pytest

from backend.database.init_db import DatabaseInitializer
from backend.repositories.faq_repository import FaqRepository


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_returns_faq_id(test_database):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    faq_id = await repository.create(
        question="Как записаться?",
        answer="Через форму на сайте.",
        position=1,
        is_hidden=False,
    )

    assert faq_id == 1


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_stores_all_fields(test_database):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    faq_id = await repository.create(
        question="Какой у вас график?",
        answer="С 09:00 до 18:00.",
        position=5,
        is_hidden=True,
    )

    faq = await repository.get_by_id(faq_id)

    assert faq == {
        "id": faq_id,
        "question": "Какой у вас график?",
        "answer": "С 09:00 до 18:00.",
        "position": 5,
        "is_hidden": 1,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_create_uses_default_values(test_database):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    faq_id = await repository.create(
        question="Как записаться?",
        answer="Через сайт.",
    )

    faq = await repository.get_by_id(faq_id)

    assert faq is not None
    assert faq["position"] == 0
    assert faq["is_hidden"] == 0


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_id_returns_faq(test_database):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    faq_id = await repository.create(
        question="Вопрос",
        answer="Ответ",
    )

    faq = await repository.get_by_id(faq_id)

    assert faq is not None
    assert faq["id"] == faq_id
    assert faq["question"] == "Вопрос"
    assert faq["answer"] == "Ответ"


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_nonexistent_faq(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    faq = await repository.get_by_id(999)

    assert faq is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_returns_empty_list_for_empty_table(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    faqs = await repository.get_all()

    assert faqs == []


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_returns_all_faqs(test_database):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    await repository.create(
        question="Первый вопрос",
        answer="Первый ответ",
    )

    await repository.create(
        question="Второй вопрос",
        answer="Второй ответ",
    )

    faqs = await repository.get_all()

    assert len(faqs) == 2
    assert faqs[0]["question"] == "Первый вопрос"
    assert faqs[1]["question"] == "Второй вопрос"


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_orders_by_position_then_id(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    first_id = await repository.create(
        question="Первый",
        answer="Ответ",
        position=2,
    )

    second_id = await repository.create(
        question="Второй",
        answer="Ответ",
        position=1,
    )

    third_id = await repository.create(
        question="Третий",
        answer="Ответ",
        position=2,
    )

    faqs = await repository.get_all()

    assert [faq["id"] for faq in faqs] == [
        second_id,
        first_id,
        third_id,
    ]


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_filters_hidden_faqs(test_database):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    await repository.create(
        question="Видимый",
        answer="Ответ",
        is_hidden=False,
    )

    await repository.create(
        question="Скрытый",
        answer="Ответ",
        is_hidden=True,
    )

    faqs = await repository.get_all(is_hidden=True)

    assert len(faqs) == 1
    assert faqs[0]["question"] == "Скрытый"
    assert faqs[0]["is_hidden"] == 1


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_filters_visible_faqs(test_database):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    await repository.create(
        question="Видимый",
        answer="Ответ",
        is_hidden=False,
    )

    await repository.create(
        question="Скрытый",
        answer="Ответ",
        is_hidden=True,
    )

    faqs = await repository.get_all(is_hidden=False)

    assert len(faqs) == 1
    assert faqs[0]["question"] == "Видимый"
    assert faqs[0]["is_hidden"] == 0


@pytest.mark.repository
@pytest.mark.asyncio
async def test_get_all_without_filter_returns_all_faqs(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    await repository.create(
        question="Видимый",
        answer="Ответ",
        is_hidden=False,
    )

    await repository.create(
        question="Скрытый",
        answer="Ответ",
        is_hidden=True,
    )

    faqs = await repository.get_all()

    assert len(faqs) == 2


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_returns_true_for_existing_faq(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    faq_id = await repository.create(
        question="Старый вопрос",
        answer="Старый ответ",
    )

    result = await repository.update(
        faq_id=faq_id,
        question="Новый вопрос",
        answer="Новый ответ",
        position=10,
        is_hidden=True,
    )

    assert result is True


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_changes_all_fields(test_database):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    faq_id = await repository.create(
        question="Старый вопрос",
        answer="Старый ответ",
        position=1,
        is_hidden=False,
    )

    await repository.update(
        faq_id=faq_id,
        question="Новый вопрос",
        answer="Новый ответ",
        position=10,
        is_hidden=True,
    )

    faq = await repository.get_by_id(faq_id)

    assert faq == {
        "id": faq_id,
        "question": "Новый вопрос",
        "answer": "Новый ответ",
        "position": 10,
        "is_hidden": 1,
    }


@pytest.mark.repository
@pytest.mark.asyncio
async def test_update_returns_false_for_nonexistent_faq(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    result = await repository.update(
        faq_id=999,
        question="Вопрос",
        answer="Ответ",
    )

    assert result is False


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_returns_true_for_existing_faq(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    faq_id = await repository.create(
        question="Вопрос",
        answer="Ответ",
    )

    result = await repository.delete(faq_id)

    assert result is True


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_removes_faq(test_database):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    faq_id = await repository.create(
        question="Вопрос",
        answer="Ответ",
    )

    await repository.delete(faq_id)

    faq = await repository.get_by_id(faq_id)

    assert faq is None


@pytest.mark.repository
@pytest.mark.asyncio
async def test_delete_returns_false_for_nonexistent_faq(
    test_database,
):
    await DatabaseInitializer.initialize()

    repository = FaqRepository()

    result = await repository.delete(999)

    assert result is False