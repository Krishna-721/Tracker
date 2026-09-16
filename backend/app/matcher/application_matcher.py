# Instead of just insert, we'll do email -> matcher -> create/update

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.applications import JobApplication


class ApplicationMatcher:
    """
    Responsible for determining whether an incoming
    email belongs to an existing application.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_existing(self, user_id: str, gmail_thread_id: str) -> Optional[JobApplication]:

        result = await self.db.execute(
            select(JobApplication).where(
                JobApplication.user_id == user_id,
                JobApplication.gmail_thread_id == gmail_thread_id,
            )
        )

        return result.scalar_one_or_none()