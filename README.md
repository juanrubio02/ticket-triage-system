# Ticket Triage System (Rules → LLM → Human Review)

Sistema de clasificación y enrutado de tickets pensado como en empresa:
- **Reglas primero** (rápido, barato y controlable)
- **LLM solo cuando hace falta** (JSON estricto + validación)
- **Human-in-the-loop** para revisión cuando la IA interviene o el riesgo es alto
- **Idempotencia real** por `X-Request-Id` (evita duplicados en reintentos)

## Flujo (arquitectura)
1) `POST /tickets` recibe el ticket
2) Clasificación:
   - `rules` → si no hay match, `llm` → si falla, `fallback`
3) Si `source=llm` o `risk=high` → `needs_review=true`
4) `POST /tickets/{id}/review` marca como revisado por humano

## Endpoints
- `GET /health`
- `POST /tickets`
- `GET /tickets/{ticket_id}`
- `POST /tickets/{ticket_id}/review`

## Ejecutar con Docker
```bash
cp .env.example .env
# Edita .env y añade tu LLM_API_KEY
docker compose up --build

# Ticket Triage System (Rules → LLM → Human Review)

Sistema de clasificación y enrutado de tickets pensado como en empresa:
- **Reglas primero** (rápido, barato y controlable)
- **LLM solo cuando hace falta** (JSON estricto + validación)
- **Human-in-the-loop** para revisión cuando la IA interviene o el riesgo es alto
- **Idempotencia real** por `X-Request-Id` (evita duplicados en reintentos)

## Flujo (arquitectura)
1) `POST /tickets` recibe el ticket
2) Clasificación:
   - `rules` → si no hay match, `llm` → si falla, `fallback`
3) Si `source=llm` o `risk=high` → `needs_review=true`
4) `POST /tickets/{id}/review` marca como revisado por humano

## Endpoints
- `GET /health`
- `POST /tickets`
- `GET /tickets/{ticket_id}`
- `POST /tickets/{ticket_id}/review`

## Ejecutar con Docker
```bash
cp .env.example .env
# Edita .env y añade tu LLM_API_KEY
docker compose up --build
