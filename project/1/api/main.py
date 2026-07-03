"""
FastAPI application entry point.

Endpoints:
    GET  /                — service banner
    GET  /health          — basic readiness + index stats
    POST /ask             — ask a question (RAG)
    POST /upload          — upload one or more documents (multipart)
    GET  /sources         — list indexed source filenames
    DEL  /sources/{name}  — drop all chunks for a source
    POST /feedback        — record thumbs up/down
    GET  /feedback/stats  — aggregate feedback counts

Run locally:
    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import shutil
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src import __version__
from src.config import settings
from src.document_loader import SUPPORTED_EXTENSIONS
from src.feedback import feedback_summary, record_feedback
from src.llm import MissingAPIKeyError
from src.logger import logger
from src.rag_chain import get_rag_chain
from src.vector_store import (
    delete_source,
    index_documents_from_files,
    list_sources,
    stats,
)

from api.schemas import (
    AskRequest,
    AskResponse,
    DeleteSourceResponse,
    FeedbackRequest,
    FeedbackResponse,
    HealthResponse,
    SourcesResponse,
    UploadResponse,
)


# --------------------------------------------------------------------------- #
# Lifespan: warm caches on startup so the first user request is fast.
# --------------------------------------------------------------------------- #
@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    logger.info(f"Starting QuestionAnswerSystem API v{__version__}")
    settings.ensure_dirs()
    try:
        # Warm the embedding model + vector store. The LLM is built lazily
        # so we don't crash here if the key is missing yet.
        from src.embeddings import get_embeddings
        from src.vector_store import get_vector_store

        get_embeddings()
        get_vector_store()
        logger.info("Embeddings + vector store ready")
    except Exception as e:  # noqa: BLE001
        logger.warning(f"Warm-up partially failed: {e}")
    yield
    logger.info("API shutting down")


app = FastAPI(
    title="QuestionAnswerSystem API",
    description=(
        "Production-ready RAG Q&A backend. Free-tier LLM (Groq) + local "
        "FAISS vector store + HuggingFace embeddings."
    ),
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------------- #
# Middleware: request timing + structured access log
# --------------------------------------------------------------------------- #
@app.middleware("http")
async def access_log(request: Request, call_next):
    t0 = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as e:  # noqa: BLE001
        logger.exception(f"Unhandled error on {request.method} {request.url.path}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "error": str(e)},
        )
    dt = (time.perf_counter() - t0) * 1000
    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code} "
        f"({dt:.0f}ms)"
    )
    return response


# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #
@app.get("/", tags=["meta"])
def root():
    return {
        "service": "QuestionAnswerSystem",
        "version": __version__,
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health():
    s = stats()
    return HealthResponse(
        version=__version__,
        total_chunks=s["total_chunks"],
        sources=s["sources"],
        embedding_model=s["embedding_model"],
        llm_model=settings.groq_model,
    )


@app.post("/ask", response_model=AskResponse, tags=["rag"])
def ask(req: AskRequest):
    try:
        chain = get_rag_chain()
    except MissingAPIKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )

    if req.top_k is not None:
        # Build an ad-hoc chain for this request so the global singleton's
        # top_k stays at the configured default.
        from src.rag_chain import RAGChain

        chain = RAGChain(top_k=req.top_k)

    response = chain.ask(req.question, session_id=req.session_id)
    return AskResponse(**response.to_dict())


@app.post("/upload", response_model=UploadResponse, tags=["index"])
async def upload(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    saved: list[Path] = []
    skipped: list[dict[str, str]] = []

    for f in files:
        ext = Path(f.filename or "").suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            skipped.append(
                {"file": f.filename or "<unnamed>", "reason": f"unsupported type {ext}"}
            )
            continue

        dest = settings.upload_dir / Path(f.filename).name  # type: ignore[arg-type]
        try:
            with dest.open("wb") as out:
                shutil.copyfileobj(f.file, out)
            saved.append(dest)
        except Exception as e:  # noqa: BLE001
            logger.exception(f"Failed to save {f.filename}")
            skipped.append(
                {"file": f.filename or "<unnamed>", "reason": f"save error: {e}"}
            )
        finally:
            await f.close()

    if not saved:
        raise HTTPException(
            status_code=400,
            detail={"message": "No valid files were uploaded", "skipped": skipped},
        )

    result = index_documents_from_files(saved)
    return UploadResponse(
        files_processed=result["files_processed"],
        documents_loaded=result["documents_loaded"],
        chunks_indexed=result["chunks_indexed"],
        total_chunks=result["total_chunks"],
        indexed_files=[p.name for p in saved],
        skipped_files=skipped,
    )


@app.get("/sources", response_model=SourcesResponse, tags=["index"])
def get_sources():
    s = stats()
    return SourcesResponse(
        sources=s["sources"],
        total_chunks=s["total_chunks"],
        embedding_model=s["embedding_model"],
    )


@app.delete(
    "/sources/{source_name}",
    response_model=DeleteSourceResponse,
    tags=["index"],
)
def delete_source_endpoint(source_name: str):
    if source_name not in list_sources():
        raise HTTPException(status_code=404, detail=f"Source '{source_name}' not found")
    n = delete_source(source_name)
    # Also remove the uploaded file from disk if present.
    file_path = settings.upload_dir / source_name
    if file_path.is_file():
        try:
            file_path.unlink()
        except OSError as e:
            logger.warning(f"Could not delete file {file_path}: {e}")
    return DeleteSourceResponse(source=source_name, chunks_deleted=n)


@app.post("/feedback", response_model=FeedbackResponse, tags=["feedback"])
def submit_feedback(req: FeedbackRequest):
    fid = record_feedback(
        question=req.question,
        answer=req.answer,
        rating=req.rating,
        sources=req.sources,
        comment=req.comment,
        session_id=req.session_id,
    )
    return FeedbackResponse(id=fid)


@app.get("/feedback/stats", tags=["feedback"])
def feedback_stats():
    return feedback_summary()
