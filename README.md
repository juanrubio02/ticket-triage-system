# Ticket Triage System — Rules → LLM → Human Review

Sistema backend de clasificación y enrutado de tickets, diseñado con criterios reales de empresa:
control de costes, fiabilidad, explicabilidad y revisión humana.

## Qué demuestra este proyecto
- Diseño de sistemas con **IA aplicada de forma responsable**
- Uso de **reglas antes que LLM** (coste, latencia, control)
- **Idempotencia real** para evitar duplicados en reintentos
- **Human-in-the-loop** cuando la IA interviene o hay riesgo
- Arquitectura limpia, modular y dockerizada

---

## Flujo de clasificación
1. `POST /tickets` recibe el ticket
2. Clasificación:
   - Reglas deterministas (`rules`)
   - Si no hay match → LLM
   - Si falla → fallback seguro
3. Si `source=llm` o `risk=high` → `needs_review=true`
4. Un humano revisa con `POST /tickets/{id}/review`

---

## Endpoints principales
- `GET /health` — estado del servicio
- `POST /tickets` — creación de ticket (idempotente)
- `GET /tickets/{ticket_id}` — consulta de ticket
- `POST /tickets/{ticket_id}/review` — revisión humana
- `GET /stats` — métricas operativas básicas

---

## Métricas (`/stats`)
Ejemplo de datos expuestos:
- Total de tickets
- Distribución por categoría
- Distribución por fuente
- Tickets pendientes de revisión humana

---

## Ejecutar con Docker
```bash
cp .env.example .env
# Añade tu LLM_API_KEY en .env
docker compose up --build
