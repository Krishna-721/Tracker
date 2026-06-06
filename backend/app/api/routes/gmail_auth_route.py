import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.db.postgres import get_db
from app.core.config import settings
from app.models.gmail_token import GmailToken

from google.oauth2 import id_token
from google.auth.transport import requests as grequests

router = APIRouter()

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
]

_flow_store = {}

CLIENT_CONFIG = {
    "web": {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
    }
}

@router.get("/auth/gmail/login")
async def gmail_login():
    flow = Flow.from_client_config(
        CLIENT_CONFIG, scopes=SCOPES, redirect_uri=settings.GOOGLE_REDIRECT_URI,
    )
    auth_url, state = flow.authorization_url(
        access_type="offline", prompt="consent",
    )
    _flow_store[state] = flow.code_verifier
    return RedirectResponse(auth_url)


@router.get("/auth/gmail/callback")
async def gmail_callback(request: Request, db: AsyncSession = Depends(get_db)):
    state = request.query_params.get("state")
    flow = Flow.from_client_config(
        CLIENT_CONFIG, scopes=SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI, state=state,
    )
    flow.code_verifier = _flow_store.pop(state, None)
    flow.fetch_token(authorization_response=str(request.url))
    credentials = flow.credentials
    id_info = id_token.verify_oauth2_token(
        credentials.id_token, grequests.Request(), settings.GOOGLE_CLIENT_ID, clock_skew_in_seconds=10)
    user_email = id_info["email"]

    token = GmailToken(
        user_id=user_email,
        token=credentials.token,
        refresh_token=credentials.refresh_token,
        token_uri=credentials.token_uri,
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scopes=json.dumps(list(credentials.scopes)),
    )
    db.add(token)
    await db.commit()

    return {"status": "gmail_connected"}