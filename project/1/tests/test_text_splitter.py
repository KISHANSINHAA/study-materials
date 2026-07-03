from __future__ import annotations

from langchain_core.documents import Document

from src.text_splitter import build_splitter, split_documents


def test_split_basic():
    long_text = ("This is a sentence. " * 200).strip()
    docs = [Document(page_content=long_text, metadata={"source": "x.txt"})]
    chunks = split_documents(docs, chunk_size=300, chunk_overlap=50)

    assert len(chunks) > 1
    for c in chunks:
        assert len(c.page_content) <= 320  # small slack for separator boundaries
        assert c.metadata["source"] == "x.txt"
        assert "chunk_id" in c.metadata
        assert "chunk_size" in c.metadata


def test_split_empty():
    assert split_documents([]) == []


def test_splitter_respects_overlap():
    splitter = build_splitter(chunk_size=100, chunk_overlap=20)
    assert splitter._chunk_size == 100
    assert splitter._chunk_overlap == 20
