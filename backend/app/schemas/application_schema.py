from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

class JobApplicationBase(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = "applied"
    source: Optional[str] = None
    notes: Optional[str] = None


class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationResponse(JobApplicationBase):
    id: int
    subject: Optional[str]=None
    created_at: datetime
    updated_at: datetime

    model_config=ConfigDict(from_attributes=True)

class EmailInput(BaseModel):
    subject: str
    body: str
    sender: str