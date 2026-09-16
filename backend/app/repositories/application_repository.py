from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.applications import JobApplication


class ApplicationRepository:
    """
    Handles all database operations for Job Applications.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_message_id(self,gmail_message_id: str) -> Optional[JobApplication]:

        result = await self.db.execute(
            select(JobApplication).where(
                JobApplication.gmail_message_id == gmail_message_id
            )
        )

        return result.scalar_one_or_none()

    async def create(self,application: JobApplication) -> JobApplication:

        self.db.add(application)

        # flush() writes changes to the current transaction so IDs become available, but the transaction isn't finalized until the service decides to commit(). That keeps related operations atomic.
        await self.db.flush()

        await self.db.refresh(application)

        return application

    async def update(self, application: JobApplication, **kwargs) -> JobApplication:

        for key, value in kwargs.items():

            setattr(application, key, value)

        await self.db.flush()

        await self.db.refresh(application)

        return application

    async def commit(self):

        await self.db.commit()

    async def delete(self, application: JobApplication):

        await self.db.delete(application)

        await self.db.flush()