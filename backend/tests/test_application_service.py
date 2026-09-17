import pytest
from unittest.mock import AsyncMock

from app.gmail.pipeline_result import PipelineResult
from app.services.application_service import ApplicationService
from app.models.applications import JobApplication


pytestmark = pytest.mark.asyncio


def make_result(
    status: str,
    thread_id: str = "thread-123",
    message_id: str = "message-123",
    ignore: bool = False,
):
    return PipelineResult(
        subject="Test email",
        body="Test email body",
        sender="recruiting@example.com",
        gmail_message_id=message_id,
        gmail_thread_id=thread_id,
        company="Google",
        role="Software Engineer",
        status=status,
        confidence=0.95,
        classification_method="RULE",
        ignore=ignore,
        ignore_reason=None,
        needs_review=False,
    )


async def test_create_new_application():
    repository = AsyncMock()
    matcher = AsyncMock()

    repository.find_by_message_id.return_value = None

    matcher.find_existing.return_value = None

    service = ApplicationService(repository, matcher)

    result = make_result("applied")

    application = await service.process(
        user_id="test@example.com",
        result=result,
    )

    assert isinstance(application, JobApplication)
    assert application.status == "applied"
    assert application.company == "Google"
    assert application.role == "Software Engineer"

    matcher.find_existing.assert_awaited_once()
    repository.create.assert_awaited_once()
    repository.commit.assert_awaited_once()


async def test_update_applied_to_interview():
    repository = AsyncMock()
    matcher = AsyncMock()

    repository.find_by_message_id.return_value = None

    existing = JobApplication(
        user_id="test@example.com",
        company="Google",
        role="Software Engineer",
        status="applied",
        gmail_thread_id="thread-123",
        gmail_message_id="old-message",
    )

    matcher.find_existing.return_value = existing

    service = ApplicationService(repository, matcher)

    result = make_result(
        "interview",
        message_id="new-message",
    )

    application = await service.process(
        user_id="test@example.com",
        result=result,
    )

    assert application is existing

    repository.update.assert_awaited_once()
    repository.commit.assert_awaited_once()
    repository.create.assert_not_awaited()

    update_kwargs = repository.update.call_args.kwargs

    assert update_kwargs["status"] == "interview"


async def test_do_not_move_interview_back_to_applied():
    repository = AsyncMock()
    matcher = AsyncMock()

    repository.find_by_message_id.return_value = None

    existing = JobApplication(
        user_id="test@example.com",
        company="Google",
        role="Software Engineer",
        status="interview",
        gmail_thread_id="thread-123",
        gmail_message_id="old-message",
    )

    matcher.find_existing.return_value = existing

    service = ApplicationService(repository, matcher)

    result = make_result(
        "applied",
        message_id="new-message",
    )

    application = await service.process(
        user_id="test@example.com",
        result=result,
    )

    assert application.status == "interview"

    update_kwargs = repository.update.call_args.kwargs

    assert "status" not in update_kwargs


async def test_interview_can_become_rejected():
    repository = AsyncMock()
    matcher = AsyncMock()

    repository.find_by_message_id.return_value = None

    existing = JobApplication(
        user_id="test@example.com",
        company="Google",
        role="Software Engineer",
        status="interview",
        gmail_thread_id="thread-123",
        gmail_message_id="old-message",
    )

    matcher.find_existing.return_value = existing

    service = ApplicationService(repository, matcher)

    result = make_result(
        "rejected",
        message_id="new-message",
    )

    application = await service.process(
        user_id="test@example.com",
        result=result,
    )

    assert application is existing

    update_kwargs = repository.update.call_args.kwargs

    assert update_kwargs["status"] == "rejected"


async def test_offer_cannot_become_rejected():
    repository = AsyncMock()
    matcher = AsyncMock()

    repository.find_by_message_id.return_value = None

    existing = JobApplication(
        user_id="test@example.com",
        company="Google",
        role="Software Engineer",
        status="offer",
        gmail_thread_id="thread-123",
        gmail_message_id="old-message",
    )

    matcher.find_existing.return_value = existing

    service = ApplicationService(repository, matcher)

    result = make_result(
        "rejected",
        message_id="new-message",
    )

    application = await service.process(
        user_id="test@example.com",
        result=result,
    )

    assert application.status == "offer"

    update_kwargs = repository.update.call_args.kwargs

    assert "status" not in update_kwargs


async def test_ignored_email_is_not_saved():
    repository = AsyncMock()
    matcher = AsyncMock()

    repository.find_by_message_id.return_value = None

    service = ApplicationService(repository, matcher)

    result = make_result(
        "applied",
        ignore=True,
    )

    application = await service.process(
        user_id="test@example.com",
        result=result,
    )

    assert application is None

    matcher.find_existing.assert_not_awaited()
    repository.create.assert_not_awaited()
    repository.update.assert_not_awaited()
    repository.commit.assert_not_awaited()

async def test_duplicate_message_is_not_processed_again():
    repository = AsyncMock()
    matcher = AsyncMock()

    repository.find_by_message_id.return_value = None

    existing = JobApplication(
        user_id="test@example.com",
        company="Google",
        role="Software Engineer",
        status="interview",
        gmail_thread_id="thread-123",
        gmail_message_id="message-123",
    )

    # The repository should tell us that this exact
    # Gmail message has already been processed.
    repository.find_by_message_id.return_value = existing

    service = ApplicationService(repository, matcher)

    result = make_result(
        "interview",
        thread_id="thread-123",
        message_id="message-123",
    )

    application = await service.process(
        user_id="test@example.com",
        result=result,
    )

    assert application is existing

    repository.find_by_message_id.assert_awaited_once_with(
        "message-123"
    )

    matcher.find_existing.assert_not_awaited()
    repository.create.assert_not_awaited()
    repository.update.assert_not_awaited()
    repository.commit.assert_not_awaited()