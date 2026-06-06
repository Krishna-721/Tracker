from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import json
from app.db.postgres import get_db

from app.core.config import settings
from app.models.gmail_token import GmailToken

from app.api.routes.emails_route import process_application
from sqlalchemy import select

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from googleapiclient.discovery import build
from app.gmail.body_parser import extract_email_body

from ml.classifier import predict_email
from ml.preprocessor import clean_email

from app.gmail.job_filter import is_spam, is_job_email
from app.models.applications import JobApplication

router=APIRouter(tags=["Sync"])

@router.get("/gmail/sync")
async def gmail_sync(user_id: str, db: AsyncSession = Depends(get_db)):
    result=await db.execute(select(GmailToken).where(GmailToken.user_id == user_id))

    gmail_token=result.scalar_one_or_none()
    if gmail_token is None: 
        raise HTTPException(status_code=404, detail="Application not found!")
    
    creds=Credentials(
        token=gmail_token.token,
        refresh_token=gmail_token.refresh_token,
        token_uri=gmail_token.token_uri,
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=json.loads(gmail_token.scopes),
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        gmail_token.token = creds.token
        await db.commit()
    
    service=build("gmail","v1", credentials=creds)
    
    response=service.users().messages().list(
        userId="me",
        maxResults=50
    ).execute()

    messages=response.get("messages",[])
    for message in messages:
        full = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute() 
        subject = ""
        sender = ""
        for h in full["payload"]["headers"]:
            if h["name"] == "Subject":
                subject = h["value"]
            elif h["name"] == "From":
                sender = h["value"]
        
        body = extract_email_body(full["payload"])
        if is_spam(subject):
            continue
        if not is_job_email(subject):
            continue
        print(f"Body length: {len(body)} | Preview: {body[:80]}")
        clean_body = clean_email(body)
        predicted_label, confidence = predict_email(subject + " " + clean_body)
        print(f"Subject: {subject[:50]} | Label: {predicted_label} | Confidence: {confidence:.2f}")
        if confidence < 0.35:
            continue
        existing=await db.execute(select(JobApplication).where(JobApplication.gmail_message_id==message["id"]))
        if existing.scalar_one_or_none() is not None:
            continue
        new_application = JobApplication(
            user_id=user_id,
            status=predicted_label,
            source=sender,
            subject=subject,
            notes=body,
            gmail_message_id=message["id"],
            gmail_thread_id=full["threadId"],
        )
        db.add(new_application)
        await db.commit()
    return {"status": "sync complete", "processed": len(messages)}