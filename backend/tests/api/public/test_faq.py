import pytest

from backend.repositories.faq_repository import FaqRepository


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_faqs_returns_visible_only(
    client,
    test_database,
) -> None:
    repository = FaqRepository()

    await repository.create(
        question="Visible question",
        answer="Visible answer",
        position=1,
        is_hidden=False,
    )

    await repository.create(
        question="Hidden question",
        answer="Hidden answer",
        position=2,
        is_hidden=True,
    )

    response = await client.get(
        "/api/faq",
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "question": "Visible question",
            "answer": "Visible answer",
            "position": 1,
            "is_hidden": False,
        },
    ]


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_faqs_returns_empty_list_when_no_visible_faqs(
    client,
    test_database,
) -> None:
    repository = FaqRepository()

    await repository.create(
        question="Hidden question",
        answer="Hidden answer",
        position=1,
        is_hidden=True,
    )

    response = await client.get(
        "/api/faq",
    )

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_faq_success(
    client,
    test_database,
) -> None:
    repository = FaqRepository()

    faq_id = await repository.create(
        question="Test question",
        answer="Test answer",
        position=1,
        is_hidden=False,
    )

    response = await client.get(
        f"/api/faq/{faq_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": faq_id,
        "question": "Test question",
        "answer": "Test answer",
        "position": 1,
        "is_hidden": False,
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_hidden_faq_returns_not_found(
    client,
    test_database,
) -> None:
    repository = FaqRepository()

    faq_id = await repository.create(
        question="Hidden question",
        answer="Hidden answer",
        position=1,
        is_hidden=True,
    )

    response = await client.get(
        f"/api/faq/{faq_id}",
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "FAQ не найден.",
    }