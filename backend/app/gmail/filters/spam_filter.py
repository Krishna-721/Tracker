SPAM_PHRASES = [
    "jobs matching your saved search",
    "job recommendations",
    "new jobs for",
    "hackathon",
    "your profile is a match",
    "apply to jobs at",
    "hiring now",
    "explore new jobs",
    "opportunities at",
    "naukri",
    "foundit",
    "matching jobs",
    "hot jobs",
    "job alert",
    "recommended jobs",
    "daily jobs",
    "saved search",
    "roles are closing",
    "save 20%",
    "coding contest",
]


def is_spam(subject: str) -> bool:
    """
    Returns True if the email is obvious spam/newsletter.
    """

    subject = subject.lower()

    return any(
        phrase in subject
        for phrase in SPAM_PHRASES
    )