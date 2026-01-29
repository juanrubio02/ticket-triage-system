from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME: str = os.getenv("APP_NAME", "ticket-triage")
ENV: str = os.getenv("ENV", "dev")
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

