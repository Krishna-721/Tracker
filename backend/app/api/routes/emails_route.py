from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from app.db.postgres import get_db

from app.models.applications import JobApplication
from app.schemas.application_schema import JobApplicationCreate, JobApplicationResponse, EmailInput

from ml.preprocessor import clean_email
# from datetime import datetime
from ml.classifier import predict_email

router = APIRouter(prefix="/emails",tags=["Emails"])

@router.post("/process",status_code=201)
async def process_application(payload: EmailInput, db: AsyncSession=Depends(get_db)):
    clean_body=clean_email(text=payload.body)

    predicted_label,confidence=predict_email(payload.subject + " "+ clean_body)
    new_application= JobApplication(
        company=None, role=None,status=predicted_label, notes=payload.body,source=payload.sender, subject=payload.subject)
    db.add(new_application)
    await db.commit()
    await db.refresh(new_application)

    return {"message": "Email received","id": new_application.id, "predicted_status": predicted_label, "confidence":confidence}