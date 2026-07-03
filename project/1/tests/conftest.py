"""
Pytest fixtures.

Every test runs against a *temporary* settings instance whose `data/` paths
point inside `tmp_path`. This keeps the developer's real index untouched.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def _isolated_data_dirs(tmp_path: Path, monkeypatch):
    """Redirect every persistent dir into a per-test tmp dir."""
    monkeypatch.setenv("VECTORSTORE_DIR", str(tmp_path / "vectorstore"))
    monkeypatch.setenv("EMBEDDING_CACHE_DIR", str(tmp_path / "cache"))
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("FEEDBACK_DIR", str(tmp_path / "feedback"))
    monkeypatch.setenv("LOG_FILE", str(tmp_path / "logs" / "test.log"))

    # Reset cached singletons so they re-read env vars.
    from src import config, vector_store, embeddings, rag_chain, llm

    config.get_settings.cache_clear()
    config.settings = config.get_settings()
    vector_store.reset_singleton()
    embeddings.get_embeddings.cache_clear()
    embeddings._base_embeddings.cache_clear()
    rag_chain.reset_rag_chain()
    llm.get_llm.cache_clear()
    yield


@pytest.fixture
def sample_txt(tmp_path: Path) -> Path:
    p = tmp_path / "sample.txt"
    p.write_text(
        "Acme Corp was founded in 1998 by Jane Smith.\n"
        "It manufactures industrial widgets and ships globally.\n"
        "The company headquarters is in Springfield.\n",
        encoding="utf-8",
    )
    return p
