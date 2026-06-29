from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import json
import logging

from app.db.postgres import get_db
from app.core.config import settings
from app.models.gmail_token import GmailToken
from app.models.applications import JobApplication

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build

from app.gmail.body_parser import extract_email_body
from app.gmail.filters.job_filter import is_spam, is_job_email

from ml.classifier import predict_email
from ml.preprocessor import clean_email

from app.gmail.classifier.classifier_rules import classify_email 

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Sync"])


@router.get("/gmail/sync")
async def gmail_sync(user_id: str, db: AsyncSession = Depends(get_db)):

    # Statistics
    processed = 0
    saved = 0
    duplicates = 0
    spam = 0
    not_job = 0
    low_confidence = 0
    errors = 0

    result = await db.execute(
        select(GmailToken).where(GmailToken.user_id == user_id)
    )

    gmail_token = result.scalar_one_or_none()

    if gmail_token is None:
        raise HTTPException(
            status_code=404,
            detail="Gmail account not connected."
        )

    creds = Credentials(
        token=gmail_token.token,
        refresh_token=gmail_token.refresh_token,
        token_uri=gmail_token.token_uri,
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=json.loads(gmail_token.scopes),
    )

    # Refresh access token if expired
    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            gmail_token.token = creds.token
            await db.commit()

        except RefreshError:
            await db.delete(gmail_token)
            await db.commit()

            raise HTTPException(
                status_code=401,
                detail="Gmail authorization expired. Please reconnect your Gmail account."
            )

    service = build("gmail", "v1", credentials=creds)

    messages = []
    page_token = None
    MAX_EMAILS=500

    while True:
        response = service.users().messages().list(
            userId="me",
            maxResults=100,
            pageToken=page_token
        ).execute()

        messages.extend(response.get("messages", []))

        page_token = response.get("nextPageToken")

        if len(messages) >= MAX_EMAILS:
            messages = messages[:MAX_EMAILS]
            break

        page_token = response.get("nextPageToken")

        if not page_token:
            break

        logger.info(f"Fetched {len(messages)} emails from Gmail.")

    for message in messages:
        processed += 1
        try:
            full = service.users().messages().get(
                userId="me",
                id=message["id"],
                format="full"
            ).execute()

            subject = ""
            sender = ""

            for header in full["payload"]["headers"]:
                if header["name"] == "Subject":
                    subject = header["value"]
                elif header["name"] == "From":
                    sender = header["value"]

            body = extract_email_body(full["payload"])

            if is_spam(subject):
                spam += 1
                continue

            # if not is_job_email(subject):
            #     not_job += 1
            #     continue

            logger.debug(f"Body Length={len(body)} | Preview={body[:80]}")

            rule_prediction = classify_email(subject, body)

            if rule_prediction:

                predicted_label = rule_prediction
                confidence = 1.0
                classification_method = "RULE"

                logger.info(f"RULE → {predicted_label}")
            else:
                clean_body = clean_email(body)
                predicted_label, confidence = predict_email(subject + " " + clean_body)

                classification_method = "ML"
                logger.info(f"ML → {predicted_label} " f"({confidence:.2f})")

            logger.info(
                f"Prediction={predicted_label} | "
                f"Confidence={confidence:.2f} | "
                f"Subject={subject[:60]}"
            )

            if confidence < 0.35:
                low_confidence += 1
                continue

            existing = await db.execute(
                select(JobApplication).where(
                    JobApplication.gmail_message_id == message["id"]))

            if existing.scalar_one_or_none():
                duplicates += 1
                continue

            application = JobApplication(
                user_id=user_id,
                status=predicted_label,
                source=sender,
                subject=subject,
                notes=body,
                gmail_message_id=message["id"],
                gmail_thread_id=full["threadId"],
            )
            db.add(application)
            saved += 1

        except Exception:
            errors += 1
            logger.exception(f"Failed processing email {message['id']}")

    # Commit once after processing all emails
    await db.commit()

    return {
        "status": "sync_complete",
        "processed": processed,
        "saved": saved,
        "duplicates": duplicates,
        "spam": spam,
        "not_job": not_job,
        "low_confidence": low_confidence,
        "errors": errors,
    }