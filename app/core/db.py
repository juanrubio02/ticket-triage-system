from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

DB_URL = os.getenv("DB_URL", "sqlite:///./data/data.db")



engine = create_engine(
    DB_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
