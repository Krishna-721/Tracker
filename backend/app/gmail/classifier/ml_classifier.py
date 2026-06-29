from ml.classifier import predict_email


def ml_classify(subject: str, body: str):
    """
    Wrapper around the ML model.
    """

    text = f"{subject} {body}"

    status, confidence = predict_email(text)

    return status, confidence