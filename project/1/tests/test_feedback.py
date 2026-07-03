from __future__ import annotations

import pytest

from src.feedback import feedback_summary, record_feedback


def test_record_and_summarise():
    fid = record_feedback(
        question="What is X?", answer="X is Y.", rating="up", session_id="s1"
    )
    assert isinstance(fid, str) and len(fid) > 0

    record_feedback(
        question="What is Z?", answer="No idea.", rating="down", session_id="s1"
    )

    summary = feedback_summary()
    assert summary["up"] == 1
    assert summary["down"] == 1
    assert summary["total"] == 2


def test_invalid_rating():
    with pytest.raises(ValueError):
        record_feedback(question="q", answer="a", rating="meh")  # type: ignore[arg-type]
