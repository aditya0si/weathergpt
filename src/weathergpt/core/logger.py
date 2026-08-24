"""Structured logging for WeatherGPT."""

import logging
import sys
from typing import Optional


def setup_logger(name: str = "weathergpt", log_level: Optional[str] = "INFO") -> logging.Logger:
    """Configures and returns a structured logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    level = getattr(logging, (log_level or "INFO").upper(), logging.INFO)
    logger.setLevel(level)
    return logger


logger = setup_logger()
