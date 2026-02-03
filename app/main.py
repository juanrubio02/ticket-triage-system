from __future__ import annotations

from fastapi import FastAPI
from app.core.config import APP_NAME, ENV
from app.api.tickets import router as tickets_router
from app.core.db import engine
from app.db.models import Base
from app.api import stats


app = FastAPI(title=APP_NAME)

app.include_router(tickets_router)
app.include_router(stats.router)



@app.get("/health")
def health():
    return {"status": "ok", "env": ENV}



@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

