# Orchestrator
# PipelineResult
#         │
#         ▼
# ApplicationMatcher
#         │
#         ▼
# Existing?
#    │            │
#   Yes          No
#    │            │
# Update       Create
#    │            │
#    └──────┬─────┘
#           ▼
# Repository.save()
#           ▼
#        Return


from app.gmail.pipeline_result import PipelineResult
from app.matcher.application_matcher import ApplicationMatcher
from app.repositories.application_repository import ApplicationRepository
from app.models.applications import JobApplication


class ApplicationService:

    def __init__(self, repository: ApplicationRepository, matcher: ApplicationMatcher):
        self.repository = repository
        self.matcher = matcher

    async def process(self, user_id: str, result: PipelineResult) -> JobApplication | None:

        # Ignore emails filtered by the pipeline
        if result.ignore:
            return None

        # Find existing application
        existing = await self.matcher.find_existing(
            user_id=user_id,
            gmail_thread_id=result.gmail_thread_id,
        )

        # -------------------------
        # UPDATE EXISTING
        # -------------------------
        if existing:

            await self.repository.update(
                existing,
                status=result.status,
                confidence=result.confidence,
                classification_method=result.classification_method,
                needs_review=result.needs_review,
                subject=result.subject,
                notes=result.body,
                source=result.sender,
                gmail_message_id=result.gmail_message_id,
                gmail_thread_id=result.gmail_thread_id,
            )

            await self.repository.commit()

            return existing

        # -------------------------
        # CREATE NEW
        # -------------------------

        application = JobApplication(
            user_id=user_id,

            company=result.company,
            role=result.role,

            status=result.status,

            subject=result.subject,
            source=result.sender,
            notes=result.body,

            confidence=result.confidence,
            classification_method=result.classification_method,
            needs_review=result.needs_review,

            gmail_message_id=result.gmail_message_id,
            gmail_thread_id=result.gmail_thread_id,
        )

        await self.repository.create(application)
        await self.repository.commit()

        return application