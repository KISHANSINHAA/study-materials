"""
Append-only feedback log.

Every user thumbs-up / thumbs-down is appended as a single JSON line to
`data/feedback/feedback.jsonl`. Append-only JSONL is trivial to ship to
S3 / BigQuery / Snowflake later for offline evaluation.
"""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from src.config import settings
from src.logger import logger


_LOG_FILE: Path = settings.feedback_dir / "feedback.jsonl"
_lock = threading.Lock()


Rating = Literal["up", "down"]


def record_feedback(
    *,
    question: str,
    answer: str,
    rating: Rating,
    sources: list[dict[str, Any]] | None = None,
    comment: str = "",
    session_id: str | None = None,
) -> str:
    """
    Append a feedback event. Returns the generated event id.
    """
    if rating not in ("up", "down"):
        raise ValueError(f"Invalid rating: {rating!r}")

    event = {
        "id": uuid4().hex,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "question": question,
        "answer": answer,
        "rating": rating,
        "comment": comment,
        "sources": sources or [],
    }

    with _lock:
        _LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with _LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")

    logger.info(f"Recorded feedback id={event['id']} rating={rating}")
    return event["id"]


def feedback_summary() -> dict[str, int]:
    """Aggregate up/down counts. Cheap enough for the small files we expect."""
    counts = {"up": 0, "down": 0, "total": 0}
    if not _LOG_FILE.exists():
        return counts

    with _LOG_FILE.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            r = ev.get("rating")
            if r in counts:
                counts[r] += 1
                counts["total"] += 1
    return counts
