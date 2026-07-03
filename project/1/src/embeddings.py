"""
Embedding model factory (stable version without CacheBackedEmbeddings)

We use HuggingFaceEmbeddings (free + local) for semantic search.
This version removes CacheBackedEmbeddings to avoid LangChain
version conflicts and import issues.

The embedding model is loaded lazily and cached for the process lifetime.
"""

from __future__ import annotations

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from src.config import settings
from src.logger import logger


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Return the embedding model used across the app.

    The first call loads the model once,
    and all future calls reuse the same instance.
    """

    logger.info(
        f"Loading embedding model '{settings.embedding_model}' "
        f"on device='{settings.embedding_device}'"
    )

    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={
            "device": settings.embedding_device
        },
        encode_kwargs={
            "normalize_embeddings": True
        },
    )