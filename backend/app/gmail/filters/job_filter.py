SPAM=[
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
    "top jobs",
    "based on your preferences",
    "opportunities waiting",
    "10+",
    "top jobs",
    "matching jobs",
    "hot job",
    "daily jobs",
    "based on your profile",
    "saved search",
    "you haven't applied",
    "roles are closing",
    "back your decisions",
    "last chance",
    "save 20%",
    "coding contest",
]

JOB_KEYWORDS = [
    "application", "interview", "offer", "internship", "hiring",
    "shortlisted", "selected", "regret", "unfortunately", "position",
    "role", "recruitment", "candidacy", "joining", "applied",
    "thank you for applying", "we regret", "pleased to inform",
    "next steps", "technical round", "coding round", "assessment"
]

def is_job_email(subject: str) -> bool:
    subject = subject.lower()
    return any(keyword in subject for keyword in JOB_KEYWORDS)

def is_spam(subject: str) -> bool:
    subject=subject.lower()
    return any(phrase in subject for phrase in SPAM)        