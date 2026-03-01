from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from app.db.postgres import get_db

from app.models.applications import JobApplication
from app.schemas.application_schema import JobApplicationCreate, JobApplicationResponse

from datetime import datetime
