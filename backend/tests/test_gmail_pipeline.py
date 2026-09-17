from app.gmail.pipeline import EmailPipeline
from app.gmail.pipeline_result import PipelineResult


def make_email(
    subject: str,
    body: str = "",
    sender: str = "recruiter@example.com",
):
    return PipelineResult(
        subject=subject,
        body=body,
        sender=sender,
        gmail_message_id="message-123",
        gmail_thread_id="thread-123",
        company="Google",
        role="Software Engineer",
    )


def test_applied_email():
    pipeline = EmailPipeline()

    email = make_email(
        subject="Application received for Software Engineer",
        body="Thank you for applying to our Software Engineer position.",
    )

    result = pipeline.process(email)

    assert result.status == "applied"
    assert result.confidence == 1.0
    assert result.classification_method == "RULE"
    assert result.ignore is False
    assert result.needs_review is False


def test_interview_email():
    pipeline = EmailPipeline()

    email = make_email(
        subject="Interview Invitation - Software Engineer",
        body="We would like to invite you to the next interview round.",
    )

    result = pipeline.process(email)

    assert result.status == "interview"
    assert result.confidence == 1.0
    assert result.classification_method == "RULE"
    assert result.ignore is False


def test_rejected_email():
    pipeline = EmailPipeline()

    email = make_email(
        subject="Update regarding your application",
        body="We regret to inform you that we will not be moving forward.",
    )

    result = pipeline.process(email)

    assert result.status == "rejected"
    assert result.confidence == 1.0
    assert result.classification_method == "RULE"
    assert result.ignore is False


def test_offer_email():
    pipeline = EmailPipeline()

    email = make_email(
        subject="Congratulations - Offer for Software Engineer",
        body="We are pleased to offer you the Software Engineer position.",
    )

    result = pipeline.process(email)

    assert result.status == "offer"
    assert result.confidence == 1.0
    assert result.classification_method == "RULE"
    assert result.ignore is False


def test_spam_email_is_ignored():
    pipeline = EmailPipeline()

    email = make_email(
        subject="Save 20% today!",
        body="Limited time offer.",
    )

    result = pipeline.process(email)

    assert result.ignore is True
    assert result.ignore_reason == "Spam"

def test_job_alert_is_ignored():
    pipeline = EmailPipeline()

    email = make_email(
        subject="Jobs for you",
        body="Here are some jobs matching your profile.",
    )

    result = pipeline.process(email)

    assert result.ignore is True
    assert result.ignore_reason in {"Spam", "Job Alert"}


def test_pipeline_preserves_gmail_metadata():
    pipeline = EmailPipeline()

    email = make_email(
        subject="Interview Invitation",
        body="We would like to interview you.",
    )

    email.gmail_message_id = "gmail-msg-456"
    email.gmail_thread_id = "gmail-thread-789"

    result = pipeline.process(email)

    assert result.gmail_message_id == "gmail-msg-456"
    assert result.gmail_thread_id == "gmail-thread-789"