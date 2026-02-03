# Ticket Triage System — Rules → LLM → Human Review

Backend system for ticket classification and routing, designed with real-world
enterprise constraints in mind: cost control, reliability, explainability and
human oversight.

## What this project demonstrates

- Applied AI system design (LLM as a component, not the whole system)
- Rules-first approach before LLM (cost, latency, control)
- Idempotent APIs to prevent duplicates on retries
- Human-in-the-loop workflow for AI-assisted decisions
- Clean, modular and dockerized backend architecture
- Basic operational metrics for observability

## Classification flow

1. `POST /tickets` receives a new ticket
2. Classification pipeline:
   - Deterministic rules
   - If no match → LLM
   - If LLM fails → safe fallback
3. If `source=llm` or `risk=high` → `needs_review=true`
4. Human review via `POST /tickets/{id}/review`

## Main endpoints

- `GET /health` — service health check
- `POST /tickets` — create ticket (idempotent)
- `GET /tickets/{ticket_id}` — retrieve ticket
- `POST /tickets/{ticket_id}/review` — human review
- `GET /stats` — operational metrics

## Metrics (`/stats`)

Exposes basic operational data:
- Total tickets processed
- Distribution by category
- Distribution by source
- Tickets pending human review

## Design decisions (why this way)

- **Rules before LLM**: predictable, cheap and auditable
- **LLM as fallback**: only used when deterministic logic fails
- **Idempotency via request_id**: consistency under retries
- **Human-in-the-loop**: required when AI intervenes or risk is elevated
- **SQLite + Docker volume**: simple, portable, production-like setup
- **Explicit logging and metrics**: observability by design

## Running with Docker

```bash
cp .env.example .env
# Add your LLM_API_KEY to .env
docker compose up --build
