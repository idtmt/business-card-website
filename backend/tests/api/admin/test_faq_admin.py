import pytest

from backend.repositories.faq_repository import FaqRepository


async def login_admin(
    client,
    admin_credentials,
) -> None:
    username, password = admin_credentials

    response = await client.post(
        "/api/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_faqs_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    await login_admin(
        client,
        admin_credentials,
    )

    repository = FaqRepository()

    await repository.create(
        question="Question 1",
        answer="Answer 1",
        position=1,
        is_hidden=False,
    )

    await repository.create(
        question="Question 2",
        answer="Answer 2",
        position=2,
        is_hidden=True,
    )

    response = await client.get(
        "/api/admin/faq",
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "question": "Question 1",
            "answer": "Answer 1",
            "position": 1,
            "is_hidden": False,
        },
        {
            "id": 2,
            "question": "Question 2",
            "answer": "Answer 2",
            "position": 2,
            "is_hidden": True,
        },
    ]


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_faqs_with_visibility_filter(
    client,
    test_database,
    admin_credentials,
) -> None:
    await login_admin(
        client,
        admin_credentials,
    )

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
        "/api/admin/faq",
        params={
            "is_hidden": True,
        },
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 2,
            "question": "Hidden question",
            "answer": "Hidden answer",
            "position": 2,
            "is_hidden": True,
        },
    ]


@pytest.mark.api
@pytest.mark.asyncio
async def test_get_faq_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    await login_admin(
        client,
        admin_credentials,
    )

    repository = FaqRepository()

    faq_id = await repository.create(
        question="Test question",
        answer="Test answer",
        position=1,
        is_hidden=False,
    )

    response = await client.get(
        f"/api/admin/faq/{faq_id}",
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
async def test_create_faq_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    await login_admin(
        client,
        admin_credentials,
    )

    response = await client.post(
        "/api/admin/faq",
        json={
            "question": "What are your working hours?",
            "answer": "We work from 09:00 to 18:00.",
            "position": 1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 201
    faq_id = response.json()

    assert isinstance(faq_id, int)

    repository = FaqRepository()

    faq = await repository.get_by_id(
        faq_id,
    )

    assert faq == {
        "id": faq_id,
        "question": "What are your working hours?",
        "answer": "We work from 09:00 to 18:00.",
        "position": 1,
        "is_hidden": False,
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_update_faq_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    await login_admin(
        client,
        admin_credentials,
    )

    repository = FaqRepository()

    faq_id = await repository.create(
        question="Old question",
        answer="Old answer",
        position=1,
        is_hidden=False,
    )

    response = await client.put(
        f"/api/admin/faq/{faq_id}",
        json={
            "question": "Updated question",
            "answer": "Updated answer",
            "position": 2,
            "is_hidden": True,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "FAQ обновлен.",
    }

    faq = await repository.get_by_id(
        faq_id,
    )

    assert faq == {
        "id": faq_id,
        "question": "Updated question",
        "answer": "Updated answer",
        "position": 2,
        "is_hidden": True,
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_delete_faq_success(
    client,
    test_database,
    admin_credentials,
) -> None:
    await login_admin(
        client,
        admin_credentials,
    )

    repository = FaqRepository()

    faq_id = await repository.create(
        question="Test question",
        answer="Test answer",
        position=1,
        is_hidden=False,
    )

    response = await client.delete(
        f"/api/admin/faq/{faq_id}",
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "FAQ удален.",
    }

    assert await repository.get_by_id(
        faq_id,
    ) is None


@pytest.mark.api
@pytest.mark.asyncio
async def test_create_faq_rejects_empty_question(
    client,
    test_database,
    admin_credentials,
) -> None:
    await login_admin(
        client,
        admin_credentials,
    )

    response = await client.post(
        "/api/admin/faq",
        json={
            "question": "",
            "answer": "Test answer",
            "position": 1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": 'Поле "question" не может быть пустым.',
    }


@pytest.mark.api
@pytest.mark.asyncio
async def test_update_faq_returns_not_found(
    client,
    test_database,
    admin_credentials,
) -> None:
    await login_admin(
        client,
        admin_credentials,
    )

    response = await client.put(
        "/api/admin/faq/999",
        json={
            "question": "Updated question",
            "answer": "Updated answer",
            "position": 1,
            "is_hidden": False,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "FAQ не найден.",
    }