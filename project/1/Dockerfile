# ---------- Builder ----------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# ---------- Runtime ----------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH \
    PORT=8501

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

RUN mkdir -p data/uploads data/vectorstore data/cache data/feedback logs

EXPOSE 8501 8000

# Default: launch the Streamlit UI. Override CMD to run the API instead.
CMD ["streamlit", "run", "app/streamlit_app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]
