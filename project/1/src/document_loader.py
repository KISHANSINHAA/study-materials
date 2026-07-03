"""
Multi-format document loader.

Supports `.pdf`, `.docx`, and `.txt` (UTF-8). Returns LangChain `Document`
objects whose metadata is normalised to:

    {
        "source":     <basename of the file>,
        "file_path":  <absolute path>,
        "file_type":  "pdf" | "docx" | "txt",
        "page":       <int, 1-indexed, only for PDF>
    }

The loader is intentionally *strict* — unknown extensions raise a
`ValueError` so callers fail loudly rather than silently dropping data.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document

from src.logger import logger


SUPPORTED_EXTENSIONS = frozenset({".pdf", ".docx", ".txt"})


class UnsupportedFileTypeError(ValueError):
    """Raised when a file's extension is not in `SUPPORTED_EXTENSIONS`."""


def _load_pdf(path: Path) -> list[Document]:
    docs = PyPDFLoader(str(path)).load()
    for d in docs:
        # `PyPDFLoader` uses 0-indexed pages; humans expect 1-indexed.
        d.metadata["page"] = int(d.metadata.get("page", 0)) + 1
        d.metadata["file_type"] = "pdf"
    return docs


def _load_docx(path: Path) -> list[Document]:
    docs = Docx2txtLoader(str(path)).load()
    for d in docs:
        d.metadata["file_type"] = "docx"
    return docs


def _load_txt(path: Path) -> list[Document]:
    docs = TextLoader(str(path), encoding="utf-8", autodetect_encoding=True).load()
    for d in docs:
        d.metadata["file_type"] = "txt"
    return docs


_LOADERS = {
    ".pdf": _load_pdf,
    ".docx": _load_docx,
    ".txt": _load_txt,
}


def load_document(path: str | Path) -> list[Document]:
    """
    Load a single document from disk.

    Parameters
    ----------
    path : str | Path
        Absolute or relative path to the file.

    Returns
    -------
    list[Document]
        One or more LangChain documents (PDFs return one per page).
    """
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        raise FileNotFoundError(f"Document not found: {p}")

    ext = p.suffix.lower()
    if ext not in _LOADERS:
        raise UnsupportedFileTypeError(
            f"Unsupported file type '{ext}'. Supported: {sorted(SUPPORTED_EXTENSIONS)}"
        )

    logger.info(f"Loading {ext} document: {p.name}")
    docs = _LOADERS[ext](p)

    for d in docs:
        d.metadata["source"] = p.name
        d.metadata["file_path"] = str(p)

    logger.info(f"Loaded {len(docs)} segment(s) from {p.name}")
    return docs


def load_documents(paths: Iterable[str | Path]) -> list[Document]:
    """Load many documents, skipping individual failures with a logged warning."""
    out: list[Document] = []
    for p in paths:
        try:
            out.extend(load_document(p))
        except (FileNotFoundError, UnsupportedFileTypeError) as e:
            logger.warning(f"Skipping {p}: {e}")
        except Exception as e:  # noqa: BLE001 — last-ditch safety net
            logger.exception(f"Failed to load {p}: {e}")
    return out
