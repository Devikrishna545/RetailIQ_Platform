# RetailIQ — Capstone Project Tracker & Requirements

> **Project:** Customer Intelligence Platform for a mid-size online retailer
> **Duration:** 10 weekends (~80 hours)
> **Datasets:** UCI Online Retail II + Amazon Fine Food Reviews
> **Stack:** Python, SQL, scikit-learn, XGBoost, PyTorch, HuggingFace, FastAPI, Streamlit, MLflow, Docker, LangChain + LLM API

---

## Table of Contents
1. [Pre-Kickoff Checklist](#pre-kickoff)
2. [Weekend-by-Weekend Tracker](#tracker)
3. [Functional Requirements](#functional-requirements)
4. [Non-Functional Requirements](#non-functional-requirements)
5. [Acceptance Criteria Summary](#acceptance-criteria)
6. [Post-Project Portfolio Polish](#portfolio)

---

<a id="pre-kickoff"></a>
## 1. Pre-Kickoff Checklist (before Weekend 1)

- [x] Install Python 3.11+, VS Code / Cursor, Git
- [x] Create GitHub repo: `retailiq-platform`
- [ ] Sign up: MLflow (local is fine), HuggingFace, Anthropic or OpenAI API key
- [x] Download datasets:
  - [x] UCI Online Retail II — https://archive.ics.uci.edu/dataset/502/online+retail+ii
  - [x] Amazon Fine Food Reviews — Kaggle
- [ ] Install Docker Desktop
- [ ] Decide time budget per weekend & put 10 slots on your calendar

---

<a id="tracker"></a>
## 2. Weekend-by-Weekend Tracker

### Weekend 1 — Foundations & Data Ingestion
**Goal:** Reproducible project skeleton + data loaded into SQLite.

**Tasks**
- [ ] Set up project with `uv` or `venv`, `pyproject.toml`, `requirements.txt`
- [ ] Create folder structure: `data/`, `notebooks/`, `src/`, `models/`, `tests/`, `api/`, `app/`
- [ ] Initialize git, add `.gitignore` (data files excluded), create `README.md` skeleton
- [ ] Add `pre-commit` with black, ruff, isort
- [ ] Write `src/data/load_retail.py` — reads Excel, writes to `data/retail.db` (SQLite)
- [ ] Write 5 exploratory SQL queries (top countries, top products, revenue/month, etc.)
- [ ] Add data dictionary to `docs/data_dictionary.md`

**Deliverable:** Repo pushed to GitHub with loader script and first SQL queries.

**Concepts mastered:** project layout, reproducibility, SQL on real data, pandas↔SQL.

**Reflection:** Write 3 sentences in `docs/learnings.md`.

---

### Weekend 2 — EDA, Statistics & Cleaning
**Goal:** Understand the data deeply; produce a clean analytical dataset.

**Tasks**
- [ ] Create `notebooks/01_eda.ipynb`
- [ ] Univariate plots: distributions of Quantity, UnitPrice, revenue
- [ ] Bivariate plots: country vs. revenue, time vs. revenue, category heatmaps
- [ ] Identify anomalies: negative quantities (returns), missing CustomerIDs, duplicates
- [ ] Run 2 hypothesis tests (e.g., t-test: UK vs. non-UK AOV; chi-square: country × return rate)
- [ ] Handle outliers (IQR or domain thresholds)
- [ ] Save cleaned dataset to `data/retail_clean.parquet`
- [ ] Write `src/data/clean.py` as a reusable function

**Deliverable:** EDA notebook with narrative + clean parquet file.

**Concepts:** pandas profiling, seaborn, scipy.stats, parquet, handling messy data.

---

### Weekend 3 — Feature Engineering & Segmentation
**Goal:** Build RFM features and segment customers.

**Tasks**
- [ ] Create `notebooks/02_segmentation.ipynb`
- [ ] Compute RFM (Recency, Frequency, Monetary) per CustomerID
- [ ] Scale with StandardScaler; try log-transform on Monetary
- [ ] K-Means: elbow method + silhouette for optimal k
- [ ] PCA 2D visualization of clusters
- [ ] Profile and name each segment (e.g., "VIPs", "At-Risk Loyalists", "One-Timers")
- [ ] Save `src/features/rfm.py` + segment labels to `data/segments.parquet`
- [ ] Compare K-Means vs. DBSCAN briefly

**Deliverable:** Segmentation notebook + labeled customers + `rfm.py` module.

**Concepts:** scaling, clustering metrics, PCA, domain-driven features.

---

### Weekend 4 — Churn Modeling (Part 1: Baseline)
**Goal:** Define churn, build a leakage-free baseline.

**Tasks**
- [ ] Define churn: "no purchase in 90 days" (or your chosen threshold) — document choice
- [ ] Create feature set: RFM + tenure + segment + derived aggregates
- [ ] Time-aware train/val/test split (past → future)
- [ ] Build sklearn `Pipeline` with `ColumnTransformer` (impute + encode + scale)
- [ ] Logistic Regression baseline
- [ ] Metrics: accuracy, precision, recall, F1, ROC-AUC, PR-AUC
- [ ] Plot ROC and PR curves; confusion matrix at chosen threshold
- [ ] Save to `src/models/churn_baseline.py`

**Deliverable:** Baseline churn model + metrics report in `reports/churn_baseline.md`.

**Concepts:** target leakage, time splits, Pipelines, metrics for imbalance.

---

### Weekend 5 — Churn Modeling (Part 2: Champion Model)
**Goal:** Beat the baseline with tuned, interpretable ensembles.

**Tasks**
- [ ] Random Forest → XGBoost → LightGBM (track each)
- [ ] Handle imbalance: `class_weight`, SMOTE (via `imbalanced-learn`) — compare
- [ ] Hyperparameter tuning with Optuna (50–100 trials)
- [ ] Set up MLflow tracking; log params/metrics/artifacts for every run
- [ ] Calibration plot + `CalibratedClassifierCV` if needed
- [ ] SHAP: global feature importance + local explanation for 3 sample customers
- [ ] Choose champion model; pickle to `models/churn_champion.pkl`
- [ ] Write `reports/churn_final.md` comparing all candidates

**Deliverable:** Tuned model + MLflow runs + SHAP analysis.

**Concepts:** boosting, Bayesian optimization, calibration, interpretability.

---

### Weekend 6 — Time Series Forecasting
**Goal:** Forecast daily/weekly revenue with proper validation.

**Tasks**
- [ ] Create `notebooks/03_forecasting.ipynb`
- [ ] Aggregate to daily revenue; check stationarity (ADF test)
- [ ] Decomposition (trend/seasonal/residual)
- [ ] Model 1: Prophet (handles seasonality + holidays out of the box)
- [ ] Model 2: SARIMA (statsmodels)
- [ ] Model 3: LightGBM with lag + rolling-window features
- [ ] Walk-forward cross-validation (not random CV)
- [ ] Compare MAE / MAPE / RMSE across models
- [ ] Save champion to `models/forecast.pkl` + `src/models/forecast.py`

**Deliverable:** Forecasting notebook + saved model + backtest results.

**Concepts:** stationarity, seasonality, walk-forward CV, ML-as-forecasting.

---

### Weekend 7 — Recommenders + NLP Part 1
**Goal:** Build recommenders + classical sentiment baseline.

**Tasks**
- [ ] Content-based: TF-IDF on product descriptions → cosine similarity → top-N
- [ ] Collaborative filtering: build user-item matrix, train ALS with `implicit` library
- [ ] Evaluate with Precision@K / Recall@K on held-out purchases
- [ ] Switch to Amazon reviews dataset
- [ ] Text preprocessing: lowercasing, tokenization, stopwords, lemmatization
- [ ] TF-IDF + Logistic Regression sentiment classifier
- [ ] Confusion matrix + classification report
- [ ] Save to `src/models/recommend.py` + `src/models/sentiment_lr.py`

**Deliverable:** Recommender module + sentiment baseline + evaluation.

**Concepts:** similarity metrics, matrix factorization, classical NLP pipeline.

---

### Weekend 8 — NLP Part 2 + Deep Learning
**Goal:** Transformers + neural tabular benchmark.

**Tasks**
- [ ] Fine-tune DistilBERT on reviews using HuggingFace `Trainer`
- [ ] Compare accuracy/F1 vs. TF-IDF + LR baseline
- [ ] Run BERTopic for topic discovery on reviews; visualize topics
- [ ] Build PyTorch tabular NN for churn (embedding for categorical, MLP)
- [ ] Compare vs. LightGBM champion — honestly report whether DL helps
- [ ] Save transformer to HuggingFace Hub or local `models/distilbert_sentiment/`
- [ ] Write `reports/nlp_comparison.md`

**Deliverable:** Fine-tuned transformer + topic report + DL-vs-GBM benchmark.

**Concepts:** transfer learning, tokenization, embeddings, when DL is (and isn't) worth it.

---

### Weekend 9 — Deployment
**Goal:** Ship a running, containerized service.

**Tasks**
- [ ] MLflow Model Registry: register champion models with versioning
- [ ] FastAPI service with endpoints:
  - `POST /predict/churn`
  - `POST /recommend`
  - `GET /forecast?horizon=30`
  - `POST /sentiment`
  - `GET /health`
- [ ] Pydantic schemas for request/response validation
- [ ] Add basic auth (API key header) + rate limiting
- [ ] Streamlit dashboard: segments view, churn lookup, forecast chart, review analyzer
- [ ] Dockerfile (multi-stage, slim base image)
- [ ] `docker-compose.yml` for API + Streamlit + MLflow UI
- [ ] GitHub Actions: lint + tests + docker build on push
- [ ] Unit tests (pytest) for data cleaning and feature engineering

**Deliverable:** `docker-compose up` launches the full app locally.

**Concepts:** model registry, API design, containerization, CI/CD, testing.

---

### Weekend 10 — AI Layer + Polish
**Goal:** Add LLM-powered features and make it portfolio-ready.

**Tasks**
- [ ] RAG chatbot: LangChain + Claude/OpenAI + Chroma/FAISS over your `reports/` docs
- [ ] Natural-language-to-SQL agent on the SQLite warehouse (with guardrails: read-only, LIMIT enforcement)
- [ ] LLM review summarizer with structured outputs (JSON schema: sentiment, topics, action items)
- [ ] Integrate AI chat into Streamlit as a sidebar
- [ ] Write comprehensive `README.md` with: architecture diagram, demo GIF, setup steps, results table
- [ ] Record 3–5 min Loom demo video
- [ ] Add `ARCHITECTURE.md` with system diagram
- [ ] Add `RESULTS.md` with final model metrics
- [ ] Clean commit history; tag `v1.0`; write release notes
- [ ] Publish LinkedIn post + blog write-up

**Deliverable:** Public GitHub repo + demo video + blog post.

**Concepts:** RAG, agents, prompt engineering, structured outputs, technical communication.

---

<a id="functional-requirements"></a>
## 3. Functional Requirements (what the system does)

### FR-1 — Data Management
- FR-1.1 System ingests raw Excel/CSV data and persists it to a SQLite warehouse.
- FR-1.2 System provides a cleaning pipeline that handles missing values, duplicates, returns, and outliers.
- FR-1.3 System exposes a parquet-based analytical dataset for downstream tasks.
- FR-1.4 System maintains a data dictionary for every table/column.

### FR-2 — Exploratory Analysis & Reporting
- FR-2.1 System produces EDA artifacts (notebooks, plots) showing distributions, trends, and correlations.
- FR-2.2 System supports hypothesis testing (t-test, chi-square) with documented results.

### FR-3 — Customer Segmentation
- FR-3.1 System computes RFM features per customer.
- FR-3.2 System assigns each customer to exactly one segment using K-Means.
- FR-3.3 System persists segment labels and provides descriptive names for each segment.

### FR-4 — Churn Prediction
- FR-4.1 System predicts probability of churn for any given customer.
- FR-4.2 System exposes a REST endpoint that returns churn probability + risk tier (low / medium / high).
- FR-4.3 System provides SHAP-based explanations for individual predictions.
- FR-4.4 Model achieves ROC-AUC ≥ 0.80 on the held-out test set.

### FR-5 — Sales Forecasting
- FR-5.1 System forecasts daily/weekly revenue up to a configurable horizon (default 30 days).
- FR-5.2 System returns point forecasts + 80%/95% confidence intervals.
- FR-5.3 Forecasting model achieves MAPE ≤ 15% on walk-forward validation.

### FR-6 — Recommendation Engine
- FR-6.1 System returns top-N product recommendations for a given customer.
- FR-6.2 System supports two strategies: content-based and collaborative filtering.
- FR-6.3 Recommender achieves Precision@10 ≥ 0.10 on held-out purchases.

### FR-7 — NLP / Sentiment Analysis
- FR-7.1 System classifies free-text reviews as positive / negative / neutral.
- FR-7.2 System surfaces dominant topics from a review corpus via BERTopic.
- FR-7.3 Transformer model achieves ≥ 5% F1 improvement over TF-IDF+LR baseline.

### FR-8 — Model Training Pipeline
- FR-8.1 System supports end-to-end retraining with a single CLI command.
- FR-8.2 System logs every training run (params, metrics, artifacts) to MLflow.
- FR-8.3 System versions models in the MLflow Model Registry.

### FR-9 — Model Serving API (FastAPI)
- FR-9.1 `/predict/churn`, `/recommend`, `/forecast`, `/sentiment`, `/health` endpoints.
- FR-9.2 All requests/responses validated via Pydantic schemas.
- FR-9.3 API returns structured error responses (RFC 7807 style).

### FR-10 — Analytics Dashboard (Streamlit)
- FR-10.1 Dashboard visualizes segments, churn risk, revenue forecasts, and sentiment trends.
- FR-10.2 Dashboard allows lookup of a single customer's profile and predictions.
- FR-10.3 Dashboard supports review-text input for on-demand sentiment analysis.

### FR-11 — AI Assistant
- FR-11.1 RAG chatbot answers questions about project reports and findings with citations.
- FR-11.2 NL→SQL agent translates natural-language questions into safe, read-only SQL queries.
- FR-11.3 LLM summarizer returns structured JSON (sentiment, topics, action items) for a batch of reviews.

### FR-12 — Experiment Tracking & Reproducibility
- FR-12.1 Every notebook/experiment is tied to a git commit and an MLflow run.
- FR-12.2 Seeds are fixed across numpy, random, torch, sklearn.

---

<a id="non-functional-requirements"></a>
## 4. Non-Functional Requirements (how the system behaves)

### NFR-1 — Performance
- Churn/sentiment prediction latency < 200 ms (p95) on a single CPU.
- Batch prediction throughput ≥ 1,000 records/sec.
- Dashboard initial load < 3 s on local network.

### NFR-2 — Scalability
- Data pipeline handles 10× current dataset size without architectural change.
- API is stateless; horizontal scaling supported behind a reverse proxy.

### NFR-3 — Reliability & Availability
- `/health` endpoint returns 200 when models are loaded.
- Graceful error handling — no crash on malformed inputs.
- Target availability for local demo: 99%.

### NFR-4 — Security & Privacy
- API requires an API key header; no endpoint is open by default.
- No PII in logs; CustomerIDs may be hashed for shared reports.
- Secrets (API keys, DB creds) loaded from `.env` — never committed.
- SQL agent is read-only; destructive statements blocked via a SQL linter.

### NFR-5 — Maintainability
- Code passes `ruff`, `black`, `isort`, and `mypy --strict` on `src/`.
- Cyclomatic complexity per function ≤ 10.
- Test coverage ≥ 60% for `src/data/` and `src/features/`.

### NFR-6 — Reproducibility
- `requirements.txt` / `pyproject.toml` pins all versions.
- Dockerfile reproduces the environment exactly.
- Seeds fixed; data versioning via DVC or commit hashes.

### NFR-7 — Observability
- Structured JSON logging (timestamp, level, module, request ID).
- API exposes basic Prometheus-compatible metrics (`/metrics`).
- MLflow tracks all model experiments end-to-end.

### NFR-8 — Portability
- Runs on macOS, Linux, Windows via Docker.
- No hard dependence on GPU — CPU-only fallback for DistilBERT inference.

### NFR-9 — Documentation
- `README.md` with setup, architecture diagram, results, and demo link.
- Every module has docstrings (Google or NumPy style).
- API auto-docs via FastAPI's `/docs` (Swagger) and `/redoc`.
- Decision log in `docs/decisions/` (ADR-style).

### NFR-10 — Cost
- Full local dev stack runs for free.
- LLM API calls capped via env-configurable daily budget.
- Optional cloud deploy estimate ≤ $20/month at demo traffic.

### NFR-11 — Usability
- Dashboard understandable by a non-technical stakeholder within 2 minutes.
- API error messages human-readable + actionable.

### NFR-12 — Ethics & Fairness
- Document potential biases in data (geography, recency).
- Report churn model performance sliced by country and customer tenure.
- LLM outputs flagged as AI-generated in the UI.

---

<a id="acceptance-criteria"></a>
## 5. Acceptance Criteria Summary

A weekend is "done" when:
- [ ] All checkbox tasks are complete.
- [ ] Code is committed to git with a meaningful message.
- [ ] Notebooks run top-to-bottom without errors.
- [ ] A 3-sentence reflection is added to `docs/learnings.md`.

The **full project** is "done" when:
- [ ] All 12 FRs demonstrably implemented.
- [ ] All 12 NFRs at least partially addressed (some, like scalability, are aspirational).
- [ ] `docker-compose up` starts API + dashboard + MLflow without manual steps.
- [ ] Public README includes architecture diagram, metrics table, and demo video.
- [ ] At least one external artifact published (blog post or LinkedIn write-up).

---

<a id="portfolio"></a>
## 6. Post-Project Portfolio Polish

- [ ] Pin the repo on your GitHub profile
- [ ] Add project card to personal site / portfolio
- [ ] Write a technical blog post (Medium / Dev.to / personal blog)
- [ ] Record a 3–5 min Loom walkthrough for recruiters
- [ ] Add a "case study" PDF summary (1–2 pages) for job applications
- [ ] Mention specific results in resume bullets (e.g., "Built churn model achieving 0.84 ROC-AUC…")
- [ ] Prepare 2 interview stories from this project (one technical deep-dive, one trade-off discussion)

---

**Good luck. Update this file as you go — treat it as a living document.**
