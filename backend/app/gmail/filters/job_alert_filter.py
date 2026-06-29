JOB_ALERT_SUBJECTS = [
    "jobs for you",
    "recommended jobs",
    "new jobs",
    "matching jobs",
    "job alert",
    "top jobs",
    "roles you may like",
]

JOB_ALERT_BODY = [
    "recommended jobs",
    "similar jobs",
    "based on your profile",
    "jobs matching your profile",
    "people also applied",
    "interview just for you"
]


def is_job_alert(subject: str, sender: str, body: str):

    subject = subject.lower()
    body = body.lower()

    if any(x in subject for x in JOB_ALERT_SUBJECTS):
        return True

    if any(x in body for x in JOB_ALERT_BODY):
        return True

    return False