from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Text, UniqueConstraint
from sqlalchemy import Boolean


class Base(DeclarativeBase):
    pass


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        UniqueConstraint("request_id", name="uq_request_id"),
    )

    ticket_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    request_id: Mapped[str] = mapped_column(String(64), nullable=False)
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    subject: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False, default="unknown")
    priority: Mapped[str] = mapped_column(String(16), nullable=False, default="medium")
    risk: Mapped[str] = mapped_column(String(16), nullable=False, default="low")
    needs_review: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

