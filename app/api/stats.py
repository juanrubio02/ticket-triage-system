from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import func

from app.core.db import SessionLocal
from app.db.models import Ticket
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger()


@router.get("/stats")
def get_stats():
    """
    Métricas operativas del sistema (uso interno).
    """
    db = SessionLocal()
    try:
        total = db.query(func.count(Ticket.ticket_id)).scalar() or 0

        by_category = dict(
            db.query(Ticket.category, func.count(Ticket.ticket_id))
            .group_by(Ticket.category)
            .all()
        )

        by_source = dict(
            db.query(Ticket.source, func.count(Ticket.ticket_id))
            .group_by(Ticket.source)
            .all()
        )

        needs_review = {
            "true": db.query(Ticket).filter(Ticket.needs_review.is_(True)).count(),
            "false": db.query(Ticket).filter(Ticket.needs_review.is_(False)).count(),
        }

        logger.info(
            "action=stats total=%s rules=%s llm=%s review_true=%s",
            total,
            by_source.get("rules", 0),
            by_source.get("llm", 0),
            needs_review["true"],
        )

        return {
            "total_tickets": total,
            "by_category": by_category,
            "by_source": by_source,
            "needs_review": needs_review,
        }
    finally:
        db.close()
