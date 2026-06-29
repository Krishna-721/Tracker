from sqlalchemy import null
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.sql import func
from app.db.postgres import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id=Column(String(255),nullable=False)
    company = Column(String(255), nullable=True)
    role = Column(String(255), nullable=True)
    status = Column(String(100), default="applied")
    source = Column(String(100), nullable=True)
    subject=Column(String(500),nullable=True)
    notes = Column(Text, nullable=True)
    confidence=Column(Float, nullable=True)
    classification_method=Column(String(20), nullable=True)
    needs_review=Column(Boolean, default=False)

    gmail_message_id = Column(String(255), nullable=True, unique=True)
    gmail_thread_id = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )