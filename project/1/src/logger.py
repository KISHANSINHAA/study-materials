"""
Structured application logging powered by `loguru`.

We configure two sinks:
  * stderr  — colourised, human-readable, level from `LOG_LEVEL`
  * file    — rotated daily, compressed, retained for 14 days

Usage:
    from src.logger import logger
    logger.info("hello")
"""

from __future__ import annotations

import sys
from loguru import logger as _logger

from src.config import settings


def _configure() -> None:
    _logger.remove()
    _logger.add(
        sys.stderr,
        level=settings.log_level,
        colorize=True,
        backtrace=False,
        diagnose=False,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
            "- <level>{message}</level>"
        ),
    )
    _logger.add(
        str(settings.log_file),
        level=settings.log_level,
        rotation="1 day",
        retention="14 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=False,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
            "{name}:{function}:{line} - {message}"
        ),
    )


_configure()
logger = _logger
