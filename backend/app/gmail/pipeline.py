from app.gmail.pipeline_result import PipelineResult

from app.gmail.filters.spam_filter import is_spam
from app.gmail.filters.job_alert_filter import is_job_alert

from app.gmail.classifier.classifier_rules import classify as rule_classify
from app.gmail.classifier.ml_classifier import classify as ml_classify

from app.gmail.decision_engine import decide


class EmailPipeline:

    def __init__(self):
        self.spam_filter = is_spam
        self.job_alert_filter = is_job_alert

        self.rule_classifier = rule_classify
        self.ml_classifier = ml_classify

        self.decision_engine = decide

    def process(self, email: PipelineResult) -> PipelineResult:

        # Stage 1 - Spam
        if self.spam_filter(email.subject):
            email.ignore = True
            email.ignore_reason = "Spam"
            return email

        # Stage 2 - Job Alerts
        if self.job_alert_filter(email.subject, email.sender, email.body):
            email.ignore = True
            email.ignore_reason = "Job Alert"
            return email

        # Stage 3 - Rule Classifier
        status = self.rule_classifier(email.subject, email.body)

        if status:
            email.status = status
            email.confidence = 1.0
            email.classification_method = "RULE"

        else:
            # Stage 4 - ML
            status, confidence = self.ml_classifier(
                email.subject,
                email.body,
            )

            email.status = status
            email.confidence = confidence
            email.classification_method = "ML"

        # Stage 5 - Decision
        email = self.decision_engine(email)

        return email