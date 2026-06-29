from dataclasses import dataclass
from typing import Optional

@dataclass
class PipelineResult:
    """
    Represents one email travelling through the processing pipeline.
    Every stage can read/update this object.
    """
    # Raw Email
    subject: str
    body: str
    sender: str

    # Gmail Metadata
    gmail_message_id: str
    gmail_thread_id: str

    # Extracted Information
    company: Optional[str] = None
    role: Optional[str] = None

    # Classification
    status: Optional[str] = None
    confidence: Optional[float] = None
    classification_method: Optional[str] = None

    # Decision Flags
    ignore: bool = False
    ignore_reason: Optional[str] = None

    needs_review: bool = False