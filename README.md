# Ticket Triage System — Rules → LLM → Human Review

Backend system for automated ticket classification and routing, designed with real-world enterprise constraints in mind: **cost control, reliability, explainability and human oversight**.

The system combines **deterministic rules**, **LLM-assisted classification**, and a **human review workflow** to safely automate ticket triage while maintaining control over risk and costs.

---

# Architecture Overview

The classification pipeline follows a **rules-first architecture**.

```
Incoming Ticket
       │
       ▼
Deterministic Rules
       │
       ├── match → classified
       │
       ▼
LLM Classification
       │
       ├── success → classified
       │
       ▼
Fallback Classification
       │
       ▼
Human Review (if required)
```

Human review is triggered when:

- classification source = `llm`
- risk level = `high`

---

# Key Features

- **Rules-first classification**
  - deterministic, cheap, auditable

- **LLM as fallback**
  - only used when deterministic logic fails

- **Idempotent API**
  - retries never create duplicate tickets

- **Human-in-the-loop workflow**
  - required for AI-assisted or high-risk cases

- **Operational metrics**
  - system behaviour visibility via `/stats`

- **Production-like backend architecture**
  - PostgreSQL database
  - Alembic migrations
  - Dockerized service

---

# Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy 2
- PostgreSQL
- Alembic
- Docker / Docker Compose
- Pytest

---

# API Endpoints

## Health Check

```
GET /health
```

Returns service status.

---

## Create Ticket (Idempotent)

```
POST /tickets
```

Creates a new ticket and runs the classification pipeline.

Idempotency is enforced using the **`X-Request-ID` header**.

If the same request is retried with the same `X-Request-ID`, the API returns the **existing ticket instead of creating a new one**.

### Example

```bash
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: example-123" \
  -d '{
        "subject": "VPN connection issue",
        "body": "User cannot connect to VPN",
        "source": "email"
      }'
```

---

## Get Ticket

```
GET /tickets/{ticket_id}
```

Returns ticket information.

---

## Review Ticket (Human-in-the-loop)

```
POST /tickets/{ticket_id}/review
```

Allows manual override of AI classification.

---

## Operational Metrics

```
GET /stats
```

Returns aggregated system statistics:

- total tickets processed
- classification distribution
- classification source distribution
- pending human reviews

---

# Database

The system uses **PostgreSQL** with schema versioning handled by **Alembic migrations**.

Tables:

```
tickets
alembic_version
```

Important constraints:

- `ticket_id` → primary key
- `request_id` → unique (idempotency guarantee)

---

# Running the Project

## Requirements

- Docker
- Docker Compose

---

## Start the stack

```bash
docker compose up --build
```

The API will be available at:

```
http://localhost:8000
```

---

## Health Check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# Database Migrations

Alembic is used for schema versioning.

### Create migration

```bash
docker compose exec api alembic revision --autogenerate -m "description"
```

### Apply migrations

```bash
docker compose exec api alembic upgrade head
```

---

# Running Tests

Integration tests verify:

- API availability
- validation behaviour
- idempotent ticket creation

Run tests with:

```bash
pytest
```

---

# Project Goals

This project demonstrates how to design **production-ready AI-assisted systems**, focusing on:

- safe AI integration
- deterministic fallbacks
- observability
- operational robustness

It is intended as a **portfolio project demonstrating backend architecture and applied AI system design**.

---

# Possible Future Improvements

- async workers for classification
- message queue (Kafka / Redis Streams)
- structured logging
- OpenTelemetry observability
- authentication
- rate limiting

---

# License

MIT
