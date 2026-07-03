"""
End-to-end RAG chain built with LangChain Expression Language (LCEL).

Flow per `ask()` call:

    1. (optional) Condense follow-up + chat_history -> standalone question
    2. Retrieve top-k chunks for the standalone question
    3. Format chunks into a single `context` string (with source tags)
    4. Stuff `context` + `question` + `chat_history` into the QA prompt
    5. Call the LLM, parse to string
    6. Return answer + the actual source documents used

The chain is built once and reused via a process-wide singleton.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

from src.llm import get_llm
from src.logger import logger
from src.memory import get_history
from src.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT, REFUSAL
from src.vector_store import as_retriever


UNKNOWN_ANSWER = REFUSAL


# --------------------------------------------------------------------------- #
# Result type
# --------------------------------------------------------------------------- #
@dataclass
class RAGResponse:
    """Structured response returned by `RAGChain.ask`."""

    answer: str
    sources: list[dict[str, Any]] = field(default_factory=list)
    standalone_question: str = ""
    latency_ms: int = 0
    is_unknown: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "answer": self.answer,
            "sources": self.sources,
            "standalone_question": self.standalone_question,
            "latency_ms": self.latency_ms,
            "is_unknown": self.is_unknown,
        }


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _format_docs(docs: list[Document]) -> str:
    """Render retrieved chunks into the prompt-friendly context block."""
    if not docs:
        return "(no relevant context found)"
    parts: list[str] = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page")
        tag = f"{src}, p.{page}" if page else src
        parts.append(f"[Document {i} | {tag}]\n{d.page_content.strip()}")
    return "\n\n---\n\n".join(parts)


def _docs_to_sources(docs: list[Document]) -> list[dict[str, Any]]:
    """Compact JSON-friendly source list for API responses + UI."""
    out = []
    for d in docs:
        out.append(
            {
                "source": d.metadata.get("source", "unknown"),
                "page": d.metadata.get("page"),
                "chunk_id": d.metadata.get("chunk_id"),
                "snippet": d.page_content[:300].strip()
                + ("..." if len(d.page_content) > 300 else ""),
            }
        )
    return out


# --------------------------------------------------------------------------- #
# Chain
# --------------------------------------------------------------------------- #
class RAGChain:
    """Encapsulates the LCEL pipeline and exposes a sync `ask()` method."""

    def __init__(self, top_k: int | None = None) -> None:
        self.llm = get_llm()
        self.retriever = as_retriever(top_k=top_k)
        # answer = (prompt -> llm -> parse_to_str). We feed it a dict.
        self._answer_pipeline: Runnable = QA_PROMPT | self.llm | StrOutputParser()
        self._condense_pipeline: Runnable = (
            CONDENSE_QUESTION_PROMPT | self.llm | StrOutputParser()
        )

    # ---- internal steps ----
    def _condense(self, question: str, chat_history: list[BaseMessage]) -> str:
        """Rewrite a follow-up into a standalone question for retrieval."""
        if not chat_history:
            return question
        try:
            standalone = self._condense_pipeline.invoke(
                {"question": question, "chat_history": chat_history}
            ).strip()
            return standalone or question
        except Exception as e:  # noqa: BLE001
            logger.warning(f"Question condensing failed, using raw: {e}")
            return question

    def _retrieve(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def _generate(
        self,
        question: str,
        context_docs: list[Document],
        chat_history: list[BaseMessage],
    ) -> str:
        return self._answer_pipeline.invoke(
            {
                "context": _format_docs(context_docs),
                "question": question,
                "chat_history": chat_history,
            }
        )

    # ---- public API ----
    def ask(self, question: str, session_id: str | None = None) -> RAGResponse:
        """
        Run the full RAG pipeline.

        Parameters
        ----------
        question : str
            The user's raw question.
        session_id : str | None
            If provided, chat history for that session is used to (a) rewrite
            the question into a standalone form for retrieval, and (b) feed
            into the answer prompt for conversational context.
        """
        if not question or not question.strip():
            return RAGResponse(answer="Please provide a question.", is_unknown=True)

        question = question.strip()
        t0 = time.perf_counter()

        history = get_history(session_id) if session_id else None
        chat_history_msgs: list[BaseMessage] = history.messages if history else []

        try:
            standalone = self._condense(question, chat_history_msgs)
            logger.info(f"Q: {question!r}  ->  standalone: {standalone!r}")

            retrieved = self._retrieve(standalone)
            answer = self._generate(standalone, retrieved, chat_history_msgs).strip()
        except Exception as e:  # noqa: BLE001
            logger.exception(f"RAG chain failed: {e}")
            return RAGResponse(
                answer=(
                    "Sorry — I hit an internal error while answering. "
                    "Please try again or rephrase the question."
                ),
                latency_ms=int((time.perf_counter() - t0) * 1000),
                is_unknown=True,
            )

        # When the model refuses, suppress sources so we don't mislead users.
        is_unknown = UNKNOWN_ANSWER.lower() in answer.lower()
        sources = [] if is_unknown else _docs_to_sources(retrieved)

        # Persist this turn for future follow-ups in the same session.
        if history is not None:
            history.add_message(HumanMessage(content=question))
            history.add_message(AIMessage(content=answer))

        latency_ms = int((time.perf_counter() - t0) * 1000)
        logger.info(
            f"Answered in {latency_ms}ms (unknown={is_unknown}, "
            f"sources={len(sources)})"
        )
        return RAGResponse(
            answer=answer,
            sources=sources,
            standalone_question=standalone,
            latency_ms=latency_ms,
            is_unknown=is_unknown,
        )


# --------------------------------------------------------------------------- #
# Singleton accessor
# --------------------------------------------------------------------------- #
@lru_cache(maxsize=1)
def get_rag_chain() -> RAGChain:
    """Process-wide singleton chain — avoids re-loading the LLM/retriever."""
    return RAGChain()


def reset_rag_chain() -> None:
    """Force the chain to be rebuilt (e.g. after settings change)."""
    get_rag_chain.cache_clear()
