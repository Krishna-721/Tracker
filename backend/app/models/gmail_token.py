from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.postgres import Base

class GmailToken(Base):
    __tablename__ = "gmail_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=False)
    token_uri = Column(Text, nullable=False)
    client_id = Column(Text, nullable=False)
    client_secret = Column(Text, nullable=False)
    scopes = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())