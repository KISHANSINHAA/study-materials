# QuestionAnswerSystem

A **production-grade Retrieval-Augmented Generation (RAG)** Q&A system built
with **LangChain (LCEL)**, a **free LLM API (Groq)**, **FAISS** as the vector
store, and a **Streamlit** UI backed by a **FastAPI** REST API.

> Upload PDFs / DOCX / TXT &rarr; ask questions &rarr; get grounded answers
> with inline citations, conversation memory, and a feedback loop.

---

## Features

| Area                    | What you get                                                         |
| ----------------------- | -------------------------------------------------------------------- |
| Document ingestion      | PDF, DOCX, TXT loaders with normalised metadata                      |
| Chunking                | `RecursiveCharacterTextSplitter` tuned for RAG (1000 / 150 default)  |
| Embeddings              | HuggingFace `all-MiniLM-L6-v2` (free, local) + on-disk LRU cache     |
| Vector store            | Persistent FAISS index with add/delete by source                     |
| Retrieval               | Configurable top-k, MMR by default, similarity-threshold optional    |
| LLM                     | Groq free tier &mdash; ultra-low latency `llama-3.3-70b-versatile`   |
| Prompt engineering      | Anti-hallucination system prompt, fixed refusal phrase, source tags  |
| Conversation            | Per-session chat history + follow-up question condensing             |
| Backend                 | FastAPI with `/ask`, `/upload`, `/sources`, `/feedback`, `/health`   |
| Frontend                | Streamlit chat UI with sources, latency, feedback buttons            |
| Bonus features          | Multi-doc querying, chat memory, thumbs-up/down feedback log         |
| Observability           | `loguru` logs (stderr + rotating file), per-request timing           |
| Tests                   | `pytest` smoke tests for loader, splitter, feedback, API             |
| Deployment              | Streamlit Cloud, Docker, `docker-compose`                            |

---

## Project structure

```
QuestionAnswerSystem/
├── api/                       # FastAPI backend
│   ├── __init__.py
│   ├── main.py                # App + routes (/ask, /upload, /feedback, ...)
│   └── schemas.py             # Pydantic request/response models
├── app/                       # Streamlit frontend
│   ├── __init__.py
│   └── streamlit_app.py
├── src/                       # Core RAG logic (framework-agnostic)
│   ├── __init__.py
│   ├── config.py              # Pydantic-settings, all tunables
│   ├── logger.py              # Loguru config (stderr + rotating file)
│   ├── document_loader.py     # PDF / DOCX / TXT
│   ├── text_splitter.py       # Recursive char splitter
│   ├── embeddings.py          # HF embeddings + CacheBackedEmbeddings
│   ├── vector_store.py        # FAISS persistent store + helpers
│   ├── llm.py                 # Groq chat model factory
│   ├── prompts.py             # Anti-hallucination + condensation prompts
│   ├── memory.py              # In-memory chat history
│   ├── feedback.py            # JSONL feedback log
│   └── rag_chain.py           # LCEL RAG pipeline (RAGChain class)
├── tests/
│   ├── conftest.py            # Isolated tmp dirs per test
│   ├── test_document_loader.py
│   ├── test_text_splitter.py
│   ├── test_feedback.py
│   └── test_api.py
├── data/
│   ├── uploads/               # User-uploaded files
│   ├── vectorstore/           # Persisted FAISS index
│   ├── cache/                 # Embedding cache (LocalFileStore)
│   └── feedback/              # feedback.jsonl
├── .streamlit/
│   ├── config.toml            # Theme + server config
│   └── secrets.toml.example   # For Streamlit Cloud
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── packages.txt               # apt packages for Streamlit Cloud
├── requirements.txt
├── run.py                     # python run.py [api|ui|both]
└── README.md
```

---

## Quick start (local)

### 1. Clone + create a virtual environment

```bash
git clone <your-repo-url> QuestionAnswerSystem
cd QuestionAnswerSystem

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env       # Windows: copy .env.example .env
```

Edit `.env` and set your **free** Groq API key
(get one at <https://console.groq.com/keys>):

```env
GROQ_API_KEY=gsk_your_key_here
```

### 4. Run

**Streamlit UI only (recommended for local dev):**

```bash
streamlit run app/streamlit_app.py
```

Open <http://localhost:8501>.

**FastAPI backend only:**

```bash
uvicorn api.main:app --reload
```

OpenAPI docs at <http://localhost:8000/docs>.

**Both (helper script):**

```bash
python run.py both
```

---

## Deploy to Streamlit Cloud

1. Push this repo to GitHub.
2. Go to <https://share.streamlit.io> &rarr; **New app**.
3. Pick your repo / branch and set **Main file** to:
   ```
   app/streamlit_app.py
   ```
4. Click **Advanced settings &rarr; Secrets** and paste:
   ```toml
   GROQ_API_KEY = "gsk_your_key_here"
   GROQ_MODEL = "llama-3.3-70b-versatile"
   EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
   EMBEDDING_DEVICE = "cpu"
   CHUNK_SIZE = 1000
   CHUNK_OVERLAP = 150
   RETRIEVAL_TOP_K = 4
   RETRIEVAL_SEARCH_TYPE = "mmr"
   LOG_LEVEL = "INFO"
   ```
5. Click **Deploy**. Streamlit Cloud will install `requirements.txt` and the
   apt packages from `packages.txt` automatically.

> **Heads-up about persistence on Streamlit Cloud.** The FAISS index lives on
> the container's local disk and is *not* guaranteed to survive restarts. For
> a fully persistent deployment, swap FAISS for a hosted vector DB (e.g.
> Pinecone, Weaviate Cloud, Supabase pgvector). The interface in
> `src/vector_store.py` is small enough to make this a one-day swap.

---

## Deploy with Docker

```bash
# Single image, both services via docker-compose
docker compose up --build
```

- UI:  <http://localhost:8501>
- API: <http://localhost:8000/docs>

---

## REST API reference

### `POST /ask`

```json
{
  "question": "When was Acme Corp founded?",
  "session_id": "user-123",
  "top_k": 4
}
```

Response:

```json
{
  "answer": "Acme Corp was founded in 1998 [source: history.pdf, p.2].",
  "sources": [
    {"source": "history.pdf", "page": 2, "chunk_id": 17, "snippet": "..."}
  ],
  "standalone_question": "When was Acme Corp founded?",
  "latency_ms": 612,
  "is_unknown": false
}
```

### `POST /upload`

`multipart/form-data` with one or more `files` fields. Supported: PDF, DOCX,
TXT. Returns indexing statistics.

### `GET /sources` / `DELETE /sources/{name}`

List or remove indexed source files.

### `POST /feedback`

```json
{
  "question": "...",
  "answer": "...",
  "rating": "up",
  "comment": "great answer",
  "sources": [],
  "session_id": "user-123"
}
```

### `GET /health`

Returns version, indexed-chunk count, and configured models.

---

## Architecture

```
                 +-----------------+        +-------------------+
  user query --> | Streamlit UI    | -----> | RAGChain (LCEL)   |
                 +-----------------+        |                   |
                          |                 | 1. Condense Q     |
                 +-----------------+        | 2. Retrieve (FAISS)
                 | FastAPI /ask    | -----> | 3. Format context |
                 +-----------------+        | 4. Prompt + Groq  |
                                            | 5. Parse + cite   |
                                            +---------+---------+
                                                      |
                          +-------+    +--------+     |
   uploaded docs -------->| Loader|--->|Splitter|---->| Embeddings (HF)
                          +-------+    +--------+     |   + on-disk cache
                                                      v
                                              +---------------+
                                              | FAISS (disk)  |
                                              +---------------+
```

### Key design decisions

- **LCEL over legacy chains.** `RetrievalQA` is deprecated; the codebase
  uses `Runnable` composition for transparency, streaming-readiness, and
  easier testing.
- **Provider-agnostic core.** `src/` knows nothing about FastAPI or
  Streamlit. Swap either frontend without touching the RAG pipeline.
- **Cached embeddings.** `CacheBackedEmbeddings` + `LocalFileStore` makes
  re-indexing the same document essentially free.
- **Singleton models.** The HuggingFace model and FAISS index are loaded
  once per process via `lru_cache`/module-level state.
- **Strict prompts.** A fixed refusal phrase (`"I don't have enough
  information ..."`) is enforced, and the chain detects it to suppress
  misleading source citations.
- **MMR retrieval.** Default search type is Max-Marginal-Relevance, which
  diversifies retrieved chunks and reduces redundancy in the prompt.

---

## Configuration reference (`.env`)

| Variable                       | Default                                             | Notes                                  |
| ------------------------------ | --------------------------------------------------- | -------------------------------------- |
| `GROQ_API_KEY`                 | _(required)_                                        | Free at console.groq.com               |
| `GROQ_MODEL`                   | `llama-3.3-70b-versatile`                           | Any Groq-hosted chat model             |
| `GROQ_TEMPERATURE`             | `0.1`                                               | Low &rarr; deterministic answers       |
| `GROQ_MAX_TOKENS`              | `1024`                                              |                                        |
| `EMBEDDING_MODEL`              | `sentence-transformers/all-MiniLM-L6-v2`            | Any HF sentence-transformer            |
| `EMBEDDING_DEVICE`             | `cpu`                                               | `cuda` / `mps` if available            |
| `CHUNK_SIZE`                   | `1000`                                              |                                        |
| `CHUNK_OVERLAP`                | `150`                                               |                                        |
| `RETRIEVAL_TOP_K`              | `4`                                                 |                                        |
| `RETRIEVAL_SEARCH_TYPE`        | `mmr`                                               | `similarity` or `mmr`                  |
| `RETRIEVAL_SCORE_THRESHOLD`    | `0.0`                                               | Used with `similarity_score_threshold` |
| `VECTORSTORE_DIR`              | `data/vectorstore`                                  | Persistent FAISS path                  |
| `EMBEDDING_CACHE_DIR`          | `data/cache`                                        | LocalFileStore for embeddings          |
| `UPLOAD_DIR`                   | `data/uploads`                                      |                                        |
| `FEEDBACK_DIR`                 | `data/feedback`                                     |                                        |
| `API_HOST` / `API_PORT`        | `0.0.0.0` / `8000`                                  |                                        |
| `LOG_LEVEL` / `LOG_FILE`       | `INFO` / `logs/app.log`                             |                                        |

---

## Running tests

```bash
pytest -q
```

Tests are hermetic: every test gets its own `tmp_path`-scoped data
directories, so they never touch your real index.

---

## Roadmap / production hardening

- Swap FAISS for a hosted vector DB (Pinecone / Weaviate / pgvector).
- Add streaming responses (`StreamingResponse` + LCEL `astream`).
- Replace in-memory chat history with Redis (`RedisChatMessageHistory`).
- Add reranking (e.g. Cohere Rerank or `bge-reranker-base`) before the LLM.
- Auth on the FastAPI layer (API keys / OAuth).
- Prometheus / OpenTelemetry instrumentation.
- Eval harness on top of the feedback log (precision, refusal rate, latency).

---
