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

def classify_email(subject: str, body: str) -> str | None:
    text = (subject + " " + body).lower()
    
    rejection_signals = [
        "not moving forward",
        "decided to move forward with other",
        "unable to proceed with your application",
        "regret to inform",
        "will not be extending an offer",
        "not been successful",
        "decided not to proceed",
        "unfortunately we have taken the decision",
        "progress with other candidates",
        "not proceeding with your candidacy",
        "unable to offer you",
        "won't be moving forward",
        "we will not be proceeding",
        "decided to move in a different direction",
    ]
    
    offer_signals = [
        "offer letter",
        "pleased to offer you",
        "we are extending an offer",
        "stipend will be",
        "confirm your acceptance",
        "sign and return",
        "joining date",
        "we are delighted to offer",
        "formally offer you",
        "excited to offer you",
    ]
    
    interview_signals = [
        "schedule a",
        "invite you for a",
        "technical interview",
        "coding round",
        "share your availability",
        "book a slot",
        "hackerrank",
        "complete the assessment",
        "shortlisted for",
        "move you to the next stage",
        "pair programming session",
        "please complete this coding",
    ]
    
    other_signals = [
        "received your application",
        "thank you for applying",
        "successfully submitted",
        "will be in touch",
        "our team will review",
        "application is being evaluated",
        "application has been submitted",
        "we have received your",
    ]
    
    if any(p in text for p in rejection_signals):
        return "rejection"
    if any(p in text for p in offer_signals):
        return "offer"
    if any(p in text for p in interview_signals):
        return "interview"
    if any(p in text for p in other_signals):
        return "other"
    
    return None