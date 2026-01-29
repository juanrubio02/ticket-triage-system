from __future__ import annotations

import json
import os
import time
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from app.models.ticket import Classification

# Cargar .env de forma explícita (Python 3.13 safe)
load_dotenv(".env")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT_SECONDS", "15"))

_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    global _client
    if _client:
        return _client
    if not LLM_API_KEY:
        raise RuntimeError("LLM_API_KEY not set")
    _client = OpenAI(api_key=LLM_API_KEY, timeout=LLM_TIMEOUT)
    return _client


def classify_with_llm(subject: str, body: str, max_retries: int = 1) -> Optional[Classification]:
    """
    Devuelve Classification validada o None si falla (para fallback).
    """
    prompt = f"""
You are classifying a support ticket.
Return ONLY valid JSON with the following schema:

{{
  "category": "access | billing | outage | other",
  "priority": "low | medium | high",
  "risk": "low | medium | high",
  "reason": "short explanation"
}}

Ticket:
SUBJECT: {subject}
BODY: {body}
"""

    client = _get_client()

    for attempt in range(max_retries + 1):
        try:
            resp = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a strict JSON generator."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0,
            )

            raw = resp.choices[0].message.content
            data = json.loads(raw)

            # Validación estricta
            return Classification(
                category=data["category"],
                priority=data["priority"],
                risk=data["risk"],
                reason=data.get("reason", ""),
                source="llm",
            )

        except (json.JSONDecodeError, ValidationError, KeyError) as e:
            # Debug temporal (puedes quitarlo luego)
            print("LLM PARSE/VALIDATION ERROR:", repr(e))
            if attempt >= max_retries:
                return None
            time.sleep(0.5)

        except Exception as e:
            # Debug temporal (puedes quitarlo luego)
            print("LLM ERROR:", repr(e))
            if attempt >= max_retries:
                return None
            time.sleep(0.5)

    return None
