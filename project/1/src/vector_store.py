"""
FAISS vector store with persistent on-disk index.

The store is a thin, *thread-safe-enough* wrapper around `langchain_community`'s
FAISS integration. It exposes the operations the rest of the app needs:

  * `add_documents`     — upsert chunks (creates the index if missing)
  * `as_retriever`      — return a configured retriever
  * `delete_source`     — drop every chunk that came from a given file
  * `list_sources`      — enumerate distinct source filenames
  * `clear`             — wipe the index from disk and memory
  * `stats`             — small dict of index health information

We persist to `settings.vectorstore_dir`. Loading at startup is lazy: the
first call constructs/loads the index, subsequent calls reuse it.
"""

from __future__ import annotations

import shutil
import threading
from pathlib import Path
from typing import Iterable

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from src.config import settings
from src.embeddings import get_embeddings
from src.logger import logger


_INDEX_FILE = "index.faiss"
_lock = threading.Lock()
_store: FAISS | None = None


# --------------------------------------------------------------------------- #
# Internal helpers
# --------------------------------------------------------------------------- #
def _index_exists(directory: Path) -> bool:
    return (directory / _INDEX_FILE).is_file()


def _load_or_create() -> FAISS:
    """Load the FAISS index from disk, or build an empty one on first use."""
    global _store
    if _store is not None:
        return _store

    embeddings = get_embeddings()
    directory = settings.vectorstore_dir

    if _index_exists(directory):
        logger.info(f"Loading FAISS index from {directory}")
        _store = FAISS.load_local(
            folder_path=str(directory),
            embeddings=embeddings,
            allow_dangerous_deserialization=True,
        )
    else:
        logger.info("No existing index found — creating an empty FAISS store")
        # FAISS requires at least one document to initialise. We seed it with
        # a single placeholder, then immediately delete it.
        seed = Document(page_content="__seed__", metadata={"source": "__seed__"})
        _store = FAISS.from_documents([seed], embeddings)
        try:
            seed_id = next(iter(_store.docstore._dict))  # type: ignore[attr-defined]
            _store.delete([seed_id])
        except Exception:  # noqa: BLE001
            logger.warning("Could not delete seed document — index may contain it")
        _persist()

    return _store


def _persist() -> None:
    """Persist the in-memory FAISS index to disk."""
    if _store is None:
        return
    settings.vectorstore_dir.mkdir(parents=True, exist_ok=True)
    _store.save_local(str(settings.vectorstore_dir))
    logger.debug(f"Persisted FAISS index to {settings.vectorstore_dir}")


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def get_vector_store() -> FAISS:
    """Return the singleton FAISS store, loading from disk if needed."""
    with _lock:
        return _load_or_create()


def add_documents(chunks: list[Document]) -> int:
    """
    Add chunks to the index and persist. Returns the number of chunks added.
    """
    if not chunks:
        return 0

    with _lock:
        store = _load_or_create()
        store.add_documents(chunks)
        _persist()

    logger.info(f"Indexed {len(chunks)} chunk(s); total docs={count_documents()}")
    return len(chunks)


def as_retriever(
    top_k: int | None = None,
    search_type: str | None = None,
    score_threshold: float | None = None,
) -> VectorStoreRetriever:
    """Return a retriever configured from settings (overridable per-call)."""
    store = get_vector_store()
    k = top_k or settings.retrieval_top_k
    st = search_type or settings.retrieval_search_type

    search_kwargs: dict = {"k": k}
    if st == "mmr":
        # `fetch_k` controls the candidate pool MMR re-ranks from.
        search_kwargs["fetch_k"] = max(k * 4, 20)
        search_kwargs["lambda_mult"] = 0.5
    elif st == "similarity_score_threshold":
        search_kwargs["score_threshold"] = (
            score_threshold
            if score_threshold is not None
            else settings.retrieval_score_threshold
        )

    return store.as_retriever(search_type=st, search_kwargs=search_kwargs)


def list_sources() -> list[str]:
    """Return the distinct `source` filenames currently indexed."""
    store = get_vector_store()
    sources = {
        d.metadata.get("source", "unknown")
        for d in store.docstore._dict.values()  # type: ignore[attr-defined]
    }
    sources.discard("__seed__")
    return sorted(sources)


def delete_source(source: str) -> int:
    """Remove every chunk whose `metadata.source == source`. Returns count."""
    with _lock:
        store = _load_or_create()
        ids_to_delete = [
            doc_id
            for doc_id, doc in store.docstore._dict.items()  # type: ignore[attr-defined]
            if doc.metadata.get("source") == source
        ]
        if not ids_to_delete:
            logger.info(f"No chunks found for source '{source}'")
            return 0

        store.delete(ids_to_delete)
        _persist()

    logger.info(f"Deleted {len(ids_to_delete)} chunk(s) for source '{source}'")
    return len(ids_to_delete)


def count_documents() -> int:
    """Total number of indexed chunks."""
    store = get_vector_store()
    return len(store.docstore._dict)  # type: ignore[attr-defined]


def clear() -> None:
    """Wipe the entire index from memory *and* disk."""
    global _store
    with _lock:
        _store = None
        if settings.vectorstore_dir.exists():
            shutil.rmtree(settings.vectorstore_dir)
            settings.vectorstore_dir.mkdir(parents=True, exist_ok=True)
        logger.warning("Vector store cleared")


def stats() -> dict:
    """Return basic health information about the index."""
    return {
        "total_chunks": count_documents(),
        "sources": list_sources(),
        "embedding_model": settings.embedding_model,
        "vectorstore_dir": str(settings.vectorstore_dir),
    }


def reset_singleton() -> None:
    """Drop the in-memory handle (forces a reload from disk on next access)."""
    global _store
    with _lock:
        _store = None


def index_documents_from_files(file_paths: Iterable[str | Path]) -> dict:
    """
    Convenience: load -> split -> index a batch of files. Idempotent per
    `source` filename — the previous version is removed before re-indexing.
    """
    from src.document_loader import load_documents
    from src.text_splitter import split_documents

    paths = [Path(p) for p in file_paths]
    for p in paths:
        delete_source(p.name)

    docs = load_documents(paths)
    chunks = split_documents(docs)
    added = add_documents(chunks)

    return {
        "files_processed": len(paths),
        "documents_loaded": len(docs),
        "chunks_indexed": added,
        "total_chunks": count_documents(),
    }
