"""
API smoke tests that don't hit the LLM.

We exercise `/health`, `/sources`, `/feedback`, and validate that `/ask`
returns a proper 503 when the Groq key is missing.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def _client():
    # Import inside the function so test fixtures have a chance to reset
    # cached singletons before the FastAPI app warms its caches.
    from api.main import app

    return TestClient(app)


def test_health_ok():
    with _client() as c:
        r = c.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "version" in body
    assert "embedding_model" in body


def test_sources_initially_empty():
    with _client() as c:
        r = c.get("/sources")
    assert r.status_code == 200
    body = r.json()
    assert body["sources"] == []
    assert body["total_chunks"] == 0


def test_feedback_endpoint():
    with _client() as c:
        r = c.post(
            "/feedback",
            json={
                "question": "q?",
                "answer": "a.",
                "rating": "up",
                "sources": [],
                "comment": "nice",
            },
        )
    assert r.status_code == 200
    assert r.json()["status"] == "recorded"


def test_ask_without_api_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "")
    # Force settings to re-read.
    from src import config, llm, rag_chain

    config.get_settings.cache_clear()
    config.settings = config.get_settings()
    llm.get_llm.cache_clear()
    rag_chain.reset_rag_chain()

    with _client() as c:
        r = c.post("/ask", json={"question": "What is X?"})
    assert r.status_code == 503
