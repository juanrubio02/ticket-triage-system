from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Header, HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.db import SessionLocal
from app.core.llm_client import classify_with_llm
from app.core.logging import get_logger
from app.core.rules import classify_with_rules
from app.db.models import Ticket
from app.models.ticket import TicketIn, TicketOut, now_utc, Classification

router = APIRouter()
logger = get_logger()


def _to_ticket_out(ticket: Ticket) -> TicketOut:
    """
    Helper para convertir el modelo SQLAlchemy a TicketOut.
    Evita duplicar el mismo return en varios sitios.
    """
    return TicketOut(
        ticket_id=ticket.ticket_id,
        request_id=ticket.request_id,
        received_at=ticket.received_at,
        status=ticket.status,
        category=ticket.category,
        priority=ticket.priority,
        risk=ticket.risk,
        needs_review=getattr(ticket, "needs_review", False),
        reviewed_at=getattr(ticket, "reviewed_at", None),
    )


@router.post("/tickets", response_model=TicketOut, status_code=201)
def create_ticket(
    payload: TicketIn,
    x_request_id: str | None = Header(default=None),
):
    """
    Crea un ticket nuevo.
    - Idempotencia: mismo request_id => mismo ticket (no duplica)
    - Clasificación: rules -> llm -> fallback
    - Human-in-the-loop: si source=llm o risk=high => needs_review=True
    """
    request_id = x_request_id or str(uuid.uuid4())
    ticket_id = f"TCK-{uuid.uuid4().hex[:10]}"

    # 1) Clasificación (rules -> llm -> fallback)
    classification = classify_with_rules(payload.subject, payload.body)

    if classification is None:
        classification = classify_with_llm(payload.subject, payload.body)

    if classification is None:
        classification = Classification(
            category="unknown",
            priority="medium",
            risk="low",
            reason="Rules and LLM failed",
            source="fallback",
        )

    # 1.1) Human-in-the-loop (revisión humana)
    needs_review = (classification.source == "llm") or (classification.risk == "high")

    logger.info(
        "request_id=%s action=classify source=%s category=%s priority=%s risk=%s needs_review=%s",
        request_id,
        classification.source,
        classification.category,
        classification.priority,
        classification.risk,
        needs_review,
    )

    # 2) Persistencia + idempotencia
    db = SessionLocal()
    try:
        ticket = Ticket(
            ticket_id=ticket_id,
            request_id=request_id,
            source=payload.source,
            subject=payload.subject,
            body=payload.body,
            status="new",
            received_at=now_utc(),
            category=classification.category,
            priority=classification.priority,
            risk=classification.risk,
            needs_review=needs_review,
            reviewed_at=None,
        )

        db.add(ticket)
        db.commit()

        logger.info(
            "request_id=%s action=create_ticket result=created ticket_id=%s",
            request_id,
            ticket_id,
        )

        return _to_ticket_out(ticket)

    except IntegrityError:
        # Ya existe un ticket con ese request_id (deduplicación real por DB)
        db.rollback()

        existing = (
            db.query(Ticket)
            .filter(Ticket.request_id == request_id)
            .first()
        )

        logger.info(
            "request_id=%s action=create_ticket result=deduplicated ticket_id=%s",
            request_id,
            existing.ticket_id,
        )

        # Importante: en idempotencia devolvemos lo que ya existe
        return _to_ticket_out(existing)

    finally:
        db.close()


@router.get("/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: str):
    """
    Devuelve un ticket por su ticket_id.
    """
    db = SessionLocal()
    ticket = (
        db.query(Ticket)
        .filter(Ticket.ticket_id == ticket_id)
        .first()
    )
    db.close()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return _to_ticket_out(ticket)


@router.post("/tickets/{ticket_id}/review", response_model=TicketOut)
def review_ticket(ticket_id: str):
    """
    Marca un ticket como revisado por humano.
    - needs_review pasa a False
    - reviewed_at se guarda con timestamp UTC
    """
    db = SessionLocal()
    ticket = (
        db.query(Ticket)
        .filter(Ticket.ticket_id == ticket_id)
        .first()
    )

    if not ticket:
        db.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Marca revisión
    ticket.needs_review = False
    ticket.reviewed_at = datetime.now(timezone.utc)

    db.commit()

    logger.info(
        "action=review_ticket result=reviewed ticket_id=%s request_id=%s",
        ticket.ticket_id,
        ticket.request_id,
    )

    out = _to_ticket_out(ticket)
    db.close()
    return out


@router.get("/health")
def health():
    """
    Endpoint simple de healthcheck.
    Si ya lo tienes en otro archivo, puedes quitarlo aquí.
    Lo dejo porque ayuda en despliegues y docker.
    """
    return {"status": "ok"}
