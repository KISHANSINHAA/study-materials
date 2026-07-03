from __future__ import annotations

from pathlib import Path

import pytest

from src.document_loader import (
    UnsupportedFileTypeError,
    load_document,
    load_documents,
)


def test_load_txt(sample_txt: Path):
    docs = load_document(sample_txt)
    assert len(docs) >= 1
    assert "Acme Corp" in docs[0].page_content
    assert docs[0].metadata["source"] == sample_txt.name
    assert docs[0].metadata["file_type"] == "txt"


def test_unsupported_extension(tmp_path: Path):
    bad = tmp_path / "image.png"
    bad.write_bytes(b"not really a png")
    with pytest.raises(UnsupportedFileTypeError):
        load_document(bad)


def test_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_document(tmp_path / "does_not_exist.txt")


def test_load_many_skips_failures(tmp_path: Path, sample_txt: Path):
    bad = tmp_path / "broken.png"
    bad.write_bytes(b"x")
    docs = load_documents([sample_txt, bad, tmp_path / "missing.txt"])
    # Only the txt is loaded; the others are logged and skipped.
    assert len(docs) >= 1
    assert all(d.metadata["file_type"] == "txt" for d in docs)
