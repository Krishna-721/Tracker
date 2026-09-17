RULES = {
    "rejected": [
        "we regret to inform",
        "unfortunately",
        "not moving forward",
        "not selected",
        "application was not selected",
        "decided not to proceed",
        "will not be moving forward",
        "position has been filled",
        "other candidates",
    ],
    "offer": [
        "offer letter",
        "job offer",
        "pleased to offer",
        "offer of employment",
        "we are delighted to offer",
        "congratulations",
        "welcome to the team",
    ],
    "interview": [
        "interview",
        "schedule an interview",
        "interview invitation",
        "interview round",
        "technical interview",
        "coding interview",
        "phone screen",
        "screening call",
        "next round",
    ],
    "applied": [
        "application received",
        "application has been received",
        "thank you for applying",
        "thanks for applying",
        "application confirmation",
        "we received your application",
        "successfully submitted",
    ],
}


def classify(subject: str, body: str) -> str | None:
    """
    Classify an email using deterministic rule-based signals.

    Returns one of:
        rejected
        offer
        interview
        applied

    Returns None when no rule matches.
    """

    text = f"{subject or ''} {body or ''}".lower()

    for status, phrases in RULES.items():
        if any(phrase in text for phrase in phrases):
            return status

    return None