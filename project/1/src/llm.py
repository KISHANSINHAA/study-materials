"""
Groq LLM factory.

Groq offers a generous free tier with very low latency, which makes it an
excellent fit for an interactive RAG UI. We expose a single `get_llm()`
helper so the rest of the codebase doesn't need to know about provider
specifics.
"""

from __future__ import annotations

from functools import lru_cache

from langchain_core.language_models import BaseChatModel
from langchain_groq import ChatGroq

from src.config import settings
from src.logger import logger


class MissingAPIKeyError(RuntimeError):
    """Raised when the Groq API key is not configured."""


@lru_cache(maxsize=1)
def get_llm() -> BaseChatModel:
    """Return a configured Groq chat model (singleton)."""
    if not settings.groq_api_key:
        raise MissingAPIKeyError(
            "GROQ_API_KEY is not set. Get a free key at "
            "https://console.groq.com/keys and add it to your .env file."
        )

    logger.info(
        f"Initialising Groq LLM model='{settings.groq_model}' "
        f"temperature={settings.groq_temperature}"
    )
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=settings.groq_temperature,
        max_tokens=settings.groq_max_tokens,
        timeout=60,
        max_retries=2,
    )
