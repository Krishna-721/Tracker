STATUS_RANK={
    "applied":1,
    "interview":2,
    "offer":3,

}

def should_update_status(current_status: str | None, incoming: str) -> bool:
    """
    Decide whether an incoming classification should update
    the application's current status.

    Status progression:

        applied -> interview -> offer

    Rejected is treated as a terminal outcome, except that it
    cannot overwrite an existing offer.
    """

    if current_status is None:
        return True

    # Rejection can replace an application/interview,
    # but should never overwrite an offer.
    if incoming == "rejected":
        return current_status != "offer"

    # Ignore unknown incoming statuses.
    if incoming not in STATUS_RANK:
        return False

    # Ignore unknown current statuses rather than making
    # an unsafe assumption about their ordering.
    if current_status not in STATUS_RANK:
        return False

    # Only move forward in the application lifecycle.
    return STATUS_RANK[incoming] > STATUS_RANK[current_status]