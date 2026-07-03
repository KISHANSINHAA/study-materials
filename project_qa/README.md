# Project Q&A Hub

This directory contains technical interview questions and answers directly mapped to the source code implementations of the three active projects in the workspace.

---

## Directory Index

### 📄 [project_1_qa.md](file:///c:/Users/sinha/OneDrive/Desktop/coding/project_qa/project_1_qa.md)
*   **Topic**: Production-grade Retrieval-Augmented Generation (RAG) Q&A System.
*   **Key Concepts Covered**:
    *   End-to-end data flow (Loader, splitter, caching, FAISS, LCEL chains).
    *   Strict anti-hallucination prompt formatting and post-inference refusal checks.
    *   On-disk embedding cache (`CacheBackedEmbeddings` + `LocalFileStore`).
    *   Question condensation using historical conversational memory.
    *   **Architecture Diagram**: RAG ingestion and inference loop.

### 📄 [project_2_qa.md](file:///c:/Users/sinha/OneDrive/Desktop/coding/project_qa/project_2_qa.md)
*   **Topic**: SentinelGuard – Time-Series Anomaly Detection System.
*   **Key Concepts Covered**:
    *   Overall system pipeline (S&P 500 log returns, training split).
    *   Clean normal sequence training filters based on variance thresholds.
    *   LSTM Autoencoder layers configuration (`RepeatVector`, `TimeDistributed`).
    *   Anomaly point post-processing (Noise Floor, Dynamic Percentile, Temporal Smoothing).
    *   **Architecture Diagram**: Data ingestion, autoencoder training, and inference pipelines.

### 📄 [project_3_qa.md](file:///c:/Users/sinha/OneDrive/Desktop/coding/project_qa/project_3_qa.md)
*   **Topic**: Retail Sales Forecasting Pipeline.
*   **Key Concepts Covered**:
    *   End-to-end modular pipeline (Data aggregation, features, evaluation, UI).
    *   Feature engineering strategy (Time, memory lags, rolling stats, momentum).
    *   Chronological train-test splitting vs. standard random K-Fold CV.
    *   Random Forest vs. XGBoost model comparison and $R^2$ variance interpretation.
    *   **Architecture Diagram**: Data loader, feature merging, training, and evaluation pipeline.
