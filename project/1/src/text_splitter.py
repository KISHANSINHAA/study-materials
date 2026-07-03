"""
Recursive text splitting tuned for RAG.

We use `RecursiveCharacterTextSplitter` with a separator hierarchy that
respects natural document boundaries (paragraphs > sentences > words). This
keeps semantically related text together inside a chunk, which materially
improves retrieval quality.

Defaults come from `src.config.settings` but every parameter can be
overridden per call.
"""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import settings
from src.logger import logger


# Tried and tested separator order for general English prose & technical docs.
_SEPARATORS = [
    "\n\n",   # paragraphs
    "\n",     # lines
    ". ",     # sentences
    "? ",
    "! ",
    "; ",
    ", ",
    " ",      # words
    "",       # characters (last resort)
]


def build_splitter(
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> RecursiveCharacterTextSplitter:
    """Construct a configured splitter."""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size or settings.chunk_size,
        chunk_overlap=chunk_overlap or settings.chunk_overlap,
        separators=_SEPARATORS,
        length_function=len,
        is_separator_regex=False,
        add_start_index=True,
    )


def split_documents(
    documents: list[Document],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[Document]:
    """
    Split documents into chunks suitable for embedding.

    A `chunk_id` is added to each chunk's metadata to make sources stable
    and addressable across re-indexing runs.
    """
    if not documents:
        return []

    splitter = build_splitter(chunk_size, chunk_overlap)
    chunks = splitter.split_documents(documents)

    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = i
        c.metadata["chunk_size"] = len(c.page_content)

    logger.info(
        f"Split {len(documents)} document(s) into {len(chunks)} chunk(s) "
        f"(size={splitter._chunk_size}, overlap={splitter._chunk_overlap})"
    )
    return chunks
