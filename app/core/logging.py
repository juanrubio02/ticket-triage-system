from __future__ import annotations

import logging
import sys
from app.core.config import LOG_LEVEL

_logger: logging.Logger | None = None


def get_logger() -> logging.Logger:
    global _logger
    if _logger:
        return _logger

    logger = logging.getLogger("ticket-triage")
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.propagate = False
    _logger = logger
    return logger

