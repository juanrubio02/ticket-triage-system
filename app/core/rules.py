from __future__ import annotations

from app.models.ticket import Classification


def classify_with_rules(subject: str, body: str) -> Classification | None:
    text = (subject + " " + body).lower()

    if "403" in text or "login" in text or "acced" in text or "sesión" in text:
        return Classification(
            category="access",
            priority="high",
            risk="low",
            reason="Keywords indicate access/login issue",
            source="rules",
        )

    if "factura" in text or "invoice" in text or "cobro" in text:
        return Classification(
            category="billing",
            priority="medium",
            risk="low",
            reason="Keywords indicate billing topic",
            source="rules",
        )

    if "caído" in text or "down" in text or "no funciona" in text:
        return Classification(
            category="outage",
            priority="high",
            risk="medium",
            reason="Keywords indicate service outage",
            source="rules",
        )

    return None
