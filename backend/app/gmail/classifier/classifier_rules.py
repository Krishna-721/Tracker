
RULES= {
        "rejection_signals" : [
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
    ],
    
    "offer_signals" : [
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
    ],
    
    "interview_signals" : [
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
    ],
    
    "other_signals" : [
        "received your application",
        "thank you for applying",
        "successfully submitted",
        "will be in touch",
        "our team will review",
        "application is being evaluated",
        "application has been submitted",
        "we have received your",
    ],
    }
    
def classify(subject: str, body: str):
    text = f"{subject} {body}".lower()

    for status, phrases in RULES.items():
        if any(p in text for p in phrases):
            return status

    return None