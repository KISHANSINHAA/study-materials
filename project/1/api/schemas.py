"""Pydantic request/response schemas for the API layer."""

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------- #
# /ask
# --------------------------------------------------------------------------- #
class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)
    session_id: Optional[str] = Field(
        default=None,
        description="Opaque client-generated id used to maintain chat history.",
    )
    top_k: Optional[int] = Field(default=None, ge=1, le=20)


class SourceItem(BaseModel):
    source: str
    page: Optional[int] = None
    chunk_id: Optional[int] = None
    snippet: str


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    standalone_question: str
    latency_ms: int
    is_unknown: bool


# --------------------------------------------------------------------------- #
# /upload
# --------------------------------------------------------------------------- #
class UploadResponse(BaseModel):
    files_processed: int
    documents_loaded: int
    chunks_indexed: int
    total_chunks: int
    indexed_files: list[str]
    skipped_files: list[dict[str, str]]


# --------------------------------------------------------------------------- #
# /sources
# --------------------------------------------------------------------------- #
class SourcesResponse(BaseModel):
    sources: list[str]
    total_chunks: int
    embedding_model: str


class DeleteSourceResponse(BaseModel):
    source: str
    chunks_deleted: int


# --------------------------------------------------------------------------- #
# /feedback
# --------------------------------------------------------------------------- #
class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: Literal["up", "down"]
    sources: list[dict[str, Any]] = Field(default_factory=list)
    comment: str = ""
    session_id: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: str
    status: Literal["recorded"] = "recorded"


# --------------------------------------------------------------------------- #
# /health
# --------------------------------------------------------------------------- #
class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    version: str
    total_chunks: int
    sources: list[str]
    embedding_model: str
    llm_model: str
