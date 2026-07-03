"""
Centralised application configuration.

All runtime tunables live here. Values are loaded from environment variables
(via a `.env` file in dev, or platform secrets in prod) using
`pydantic-settings`, which gives us validation and type-coercion for free.

This module is import-safe: it does not perform any I/O on import beyond
reading environment variables and creating directories.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Strongly-typed application settings."""

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---- LLM ----
    groq_api_key: str = Field(default="", description="Groq API key")
    groq_model: str = Field(default="llama-3.3-70b-versatile")
    groq_temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    groq_max_tokens: int = Field(default=1024, gt=0)

    # ---- Embeddings ----
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2"
    )
    embedding_device: Literal["cpu", "cuda", "mps"] = Field(default="cpu")

    # ---- Storage paths (relative to project root) ----
    vectorstore_dir: Path = Field(default=Path("data/vectorstore"))
    embedding_cache_dir: Path = Field(default=Path("data/cache"))
    upload_dir: Path = Field(default=Path("data/uploads"))
    feedback_dir: Path = Field(default=Path("data/feedback"))

    # ---- Chunking ----
    chunk_size: int = Field(default=1000, gt=0)
    chunk_overlap: int = Field(default=150, ge=0)

    # ---- Retrieval ----
    retrieval_top_k: int = Field(default=4, gt=0)
    retrieval_score_threshold: float = Field(default=0.0, ge=0.0, le=1.0)
    retrieval_search_type: Literal["similarity", "mmr"] = Field(default="mmr")

    # ---- API ----
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000, gt=0, lt=65536)
    api_base_url: str = Field(default="http://localhost:8000")

    # ---- Logging ----
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO"
    )
    log_file: Path = Field(default=Path("logs/app.log"))

    # ---- Validators ----
    @field_validator(
        "vectorstore_dir",
        "embedding_cache_dir",
        "upload_dir",
        "feedback_dir",
        "log_file",
        mode="after",
    )
    @classmethod
    def _resolve_path(cls, v: Path) -> Path:
        """Resolve relative paths against the project root."""
        return v if v.is_absolute() else (PROJECT_ROOT / v).resolve()

    def ensure_dirs(self) -> None:
        """Create all required directories on disk (idempotent)."""
        for p in (
            self.vectorstore_dir,
            self.embedding_cache_dir,
            self.upload_dir,
            self.feedback_dir,
            self.log_file.parent,
        ):
            p.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a process-wide singleton `Settings` instance."""
    settings = Settings()
    settings.ensure_dirs()
    return settings


settings = get_settings()
