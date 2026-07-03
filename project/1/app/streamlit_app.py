"""
Streamlit frontend for the QuestionAnswerSystem.

The UI talks to the RAG core *directly* (in-process) rather than via HTTP.
This makes Streamlit Cloud deployment a single-process affair (no need to
also run a FastAPI server) and shaves ~50-150ms off every request.

If you want the HTTP path instead, set `USE_REMOTE_API = True` and make
sure `API_BASE_URL` points at your running FastAPI instance.

Run:
    streamlit run app/streamlit_app.py
"""

from __future__ import annotations

import sys
import time
import uuid
from pathlib import Path

# Make `src/` importable when running `streamlit run app/streamlit_app.py`.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st  # noqa: E402

from src.config import settings  # noqa: E402
from src.feedback import record_feedback  # noqa: E402
from src.llm import MissingAPIKeyError  # noqa: E402
from src.logger import logger  # noqa: E402
from src.memory import clear_history  # noqa: E402
from src.rag_chain import get_rag_chain  # noqa: E402
from src.vector_store import (  # noqa: E402
    delete_source,
    index_documents_from_files,
    list_sources,
    stats,
)


# --------------------------------------------------------------------------- #
# Page setup
# --------------------------------------------------------------------------- #
st.set_page_config(
    page_title="QuestionAnswerSystem — RAG Q&A",
    page_icon="*",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject minimal modern styling.
st.markdown(
    """
    <style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 4rem; max-width: 1100px; }
    .stChatMessage { padding: 0.4rem 0.2rem; }
    .source-card {
        background: rgba(127,127,127,0.08);
        border: 1px solid rgba(127,127,127,0.2);
        border-radius: 10px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 0.88rem;
        line-height: 1.45;
    }
    .source-card .src-meta {
        font-weight: 600;
        margin-bottom: 4px;
        color: #4b8bff;
    }
    .answer-meta {
        color: #888;
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }
    .stat-pill {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        background: rgba(75,139,255,0.15);
        color: #4b8bff;
        font-size: 0.78rem;
        margin-right: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------------------------------- #
# Session state initialisation
# --------------------------------------------------------------------------- #
def _init_state() -> None:
    if "session_id" not in st.session_state:
        st.session_state.session_id = uuid.uuid4().hex
    if "messages" not in st.session_state:
        # Each message: {"role": "user"|"assistant", "content": str,
        #                "sources": [...], "latency_ms": int, "is_unknown": bool,
        #                "id": str, "feedback": "up"|"down"|None,
        #                "question": str (only for assistant)}
        st.session_state.messages = []
    if "indexed_filenames" not in st.session_state:
        st.session_state.indexed_filenames = set()


_init_state()


# --------------------------------------------------------------------------- #
# Cached resources
# --------------------------------------------------------------------------- #
@st.cache_resource(show_spinner="Loading RAG engine ...")
def _load_chain():
    return get_rag_chain()


# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.markdown("### *  QuestionAnswerSystem")
    st.caption("RAG Q&A over your own documents")

    if not settings.groq_api_key:
        st.error(
            "**GROQ_API_KEY is not set.**\n\n"
            "Get a free key at [console.groq.com](https://console.groq.com/keys) "
            "and add it to your `.env` file (or Streamlit Cloud Secrets)."
        )

    st.divider()
    st.markdown("#### Upload documents")
    uploaded = st.file_uploader(
        "PDF, DOCX or TXT",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    if uploaded and st.button("Index uploaded files", type="primary", use_container_width=True):
        saved_paths: list[Path] = []
        with st.spinner("Saving and indexing..."):
            for f in uploaded:
                if f.name in st.session_state.indexed_filenames:
                    continue
                dest = settings.upload_dir / f.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                with dest.open("wb") as out:
                    out.write(f.getbuffer())
                saved_paths.append(dest)

            if saved_paths:
                t0 = time.perf_counter()
                result = index_documents_from_files(saved_paths)
                dt = time.perf_counter() - t0
                for p in saved_paths:
                    st.session_state.indexed_filenames.add(p.name)
                st.success(
                    f"Indexed **{result['chunks_indexed']}** chunks from "
                    f"**{result['files_processed']}** file(s) in {dt:.1f}s."
                )
            else:
                st.info("All selected files are already indexed.")

    st.divider()
    st.markdown("#### Indexed sources")
    try:
        s = stats()
        st.markdown(
            f"<span class='stat-pill'>{s['total_chunks']} chunks</span>"
            f"<span class='stat-pill'>{len(s['sources'])} files</span>",
            unsafe_allow_html=True,
        )
        if s["sources"]:
            for src in s["sources"]:
                col_a, col_b = st.columns([5, 1])
                col_a.markdown(f"- {src}")
                if col_b.button("X", key=f"del-{src}", help=f"Remove {src}"):
                    delete_source(src)
                    st.session_state.indexed_filenames.discard(src)
                    file_path = settings.upload_dir / src
                    if file_path.is_file():
                        try:
                            file_path.unlink()
                        except OSError:
                            pass
                    st.rerun()
        else:
            st.caption("No documents indexed yet.")
    except Exception as e:  # noqa: BLE001
        st.warning(f"Could not load index stats: {e}")

    st.divider()
    st.markdown("#### Settings")
    top_k = st.slider("Top-K retrieved chunks", 1, 10, settings.retrieval_top_k)
    st.caption(f"LLM: `{settings.groq_model}`")
    st.caption(f"Embeddings: `{settings.embedding_model.split('/')[-1]}`")

    st.divider()
    if st.button("Clear chat history", use_container_width=True):
        clear_history(st.session_state.session_id)
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------------------------------- #
# Main panel
# --------------------------------------------------------------------------- #
st.title("Ask your documents")
st.caption(
    "Upload PDFs, Word, or text files in the sidebar, then ask questions. "
    "Answers are grounded in your documents and include citations."
)

if not list_sources():
    st.info("Upload at least one document from the sidebar to get started.")


def _render_sources(sources: list[dict]) -> None:
    if not sources:
        return
    with st.expander(f"Sources ({len(sources)})", expanded=False):
        for i, s in enumerate(sources, 1):
            page = f" - p.{s['page']}" if s.get("page") else ""
            snippet = (s.get("snippet") or "").replace("\n", " ").strip()
            st.markdown(
                f"<div class='source-card'>"
                f"<div class='src-meta'>{i}. {s['source']}{page}</div>"
                f"<div>{snippet}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )


def _render_feedback_buttons(msg_idx: int) -> None:
    msg = st.session_state.messages[msg_idx]
    current = msg.get("feedback")
    c1, c2, c3 = st.columns([1, 1, 12])
    up_label = "[+] Helpful" if current != "up" else "[+] Helpful (sent)"
    down_label = "[-] Not helpful" if current != "down" else "[-] Not helpful (sent)"
    if c1.button(up_label, key=f"up-{msg['id']}", disabled=current is not None):
        record_feedback(
            question=msg.get("question", ""),
            answer=msg["content"],
            rating="up",
            sources=msg.get("sources", []),
            session_id=st.session_state.session_id,
        )
        msg["feedback"] = "up"
        st.rerun()
    if c2.button(down_label, key=f"down-{msg['id']}", disabled=current is not None):
        record_feedback(
            question=msg.get("question", ""),
            answer=msg["content"],
            rating="down",
            sources=msg.get("sources", []),
            session_id=st.session_state.session_id,
        )
        msg["feedback"] = "down"
        st.rerun()


# Render chat history
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            meta = []
            if "latency_ms" in msg:
                meta.append(f"{msg['latency_ms']} ms")
            if msg.get("is_unknown"):
                meta.append("no answer in context")
            if meta:
                st.markdown(
                    f"<div class='answer-meta'>{' &middot; '.join(meta)}</div>",
                    unsafe_allow_html=True,
                )
            _render_sources(msg.get("sources", []))
            _render_feedback_buttons(idx)


# Chat input
question = st.chat_input("Ask a question about your documents...")
if question:
    if not list_sources():
        st.warning("Please upload at least one document first.")
        st.stop()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
            "id": uuid.uuid4().hex,
        }
    )
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_Thinking..._")
        try:
            chain = _load_chain()
            # Honour the sidebar top_k slider for this request.
            from src.rag_chain import RAGChain

            request_chain = (
                chain if top_k == settings.retrieval_top_k else RAGChain(top_k=top_k)
            )
            response = request_chain.ask(
                question, session_id=st.session_state.session_id
            )
        except MissingAPIKeyError as e:
            placeholder.error(str(e))
            st.stop()
        except Exception as e:  # noqa: BLE001
            logger.exception("Streamlit RAG call failed")
            placeholder.error(f"Something went wrong: {e}")
            st.stop()

        placeholder.markdown(response.answer)
        st.markdown(
            f"<div class='answer-meta'>{response.latency_ms} ms"
            + (" &middot; no answer in context" if response.is_unknown else "")
            + "</div>",
            unsafe_allow_html=True,
        )
        _render_sources(response.sources)

        msg_id = uuid.uuid4().hex
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response.answer,
                "sources": response.sources,
                "latency_ms": response.latency_ms,
                "is_unknown": response.is_unknown,
                "question": question,
                "id": msg_id,
                "feedback": None,
            }
        )
        # Re-run so the feedback buttons render correctly bound to the new msg.
        st.rerun()
