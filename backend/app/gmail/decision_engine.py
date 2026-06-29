from app.gmail.pipeline_result import PipelineResult

HIGH_CONFIDENCE = 0.80
MEDIUM_CONFIDENCE = 0.50

def decide(email: PipelineResult) -> PipelineResult:
    """
    Final decision maker of the pipeline.

    Receives a classified email and decides
    whether it should be saved, ignored,
    or marked for manual review.
    """

    # ----------------------------------
    # Already ignored by previous stages
    # ----------------------------------
    if email.ignore:
        return email

    # ----------------------------------
    # Rule Engine predictions
    # ----------------------------------
    if email.classification_method == "RULE":

        email.ignore = False
        email.needs_review = False

        return email

    # ----------------------------------
    # ML Predictions
    # ----------------------------------
    if email.classification_method == "ML":

        confidence = email.confidence or 0.0

        if confidence >= HIGH_CONFIDENCE:

            email.ignore = False
            email.needs_review = False

        elif confidence >= MEDIUM_CONFIDENCE:

            email.ignore = False
            email.needs_review = True

        else:

            email.ignore = True
            email.ignore_reason = "Low Confidence"

    return email