from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

class JobApplicationBase(BaseModel):
    user_id: str
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = "applied"
    source: Optional[str] = None
    notes: Optional[str] = None


class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationResponse(JobApplicationBase):
    id: int
    
    subject: Optional[str] = None

    confidence: Optional[float] = None
    classification_method: Optional[str] = None
    needs_review: bool
    created_at: datetime
    updated_at: datetime 

    model_config = ConfigDict(from_attributes=True)

class EmailInput(BaseModel):
    subject: str
    body: str
    sender: str