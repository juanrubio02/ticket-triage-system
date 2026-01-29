from __future__ import annotations

from datetime import datetime, timezone
from pydantic import BaseModel, Field


class TicketIn(BaseModel):
    source: str = Field(..., examples=["email", "web", "api"])
    subject: str = Field(..., min_length=3, max_length=200)
    body: str = Field(..., min_length=1, max_length=20_000)


class TicketOut(BaseModel):
    ticket_id: str
    request_id: str
    received_at: datetime
    status: str = "new"

    category: str = "unknown"
    priority: str = "medium"
    risk: str = "low"

    # Human-in-the-loop
    needs_review: bool = False
    reviewed_at: datetime | None = None


class Classification(BaseModel):
    category: str
    priority: str
    risk: str
    reason: str
    source: str  # "rules" | "llm" | "fallback"


def now_utc() -> datetime:
    return datetime.now(timezone.utc)
