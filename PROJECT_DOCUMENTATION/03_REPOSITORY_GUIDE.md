# 03. Repository Guide

This document maps out the file layout, folder hierarchies, and module ownership rules for the Aditya-L1 monorepo.

---

## 🌳 Repository Tree

```
aditya-l1-monorepo/
├── backend/                        # FastAPI Gateway, AI Engine & Physics Engine
│   ├── aditya_flare/               # Core AI modules (XGBoost, TCN, Ensemble)
│   │   ├── ai_engine/              # Prediction models & pipeline definitions
│   │   ├── calibration/            # Conformal calibration & GOES mapping
│   │   ├── config/                 # YAML configs for thresholding/horizons
│   │   ├── decision/               # Mission state decision engine
│   │   ├── evaluation/             # Model metrics, ROC, Confusion Matrix
│   │   └── models/                 # XGBoost, Forecaster modules
│   ├── api/                        # REST Gateway routers & WebSocket endpoints
│   │   ├── routes/                 # Module routers (dashboard, forecast, kg, physics)
│   │   └── ws/                     # Live streaming Websocket gateway
│   ├── data/                       # Local database, raw telemetry, model weights
│   │   ├── feature_store/          # Saved parquet datasets
│   │   └── models/                 # Model checkpoints (ensemble_forecaster.pkl)
│   ├── events/                     # PubSub Event Bus & telemetry simulator
│   ├── physics_engine/             # Thermodynamics, Wavelets, & Spectras
│   ├── reasoning/                  # AI Scientist SRE LangGraph agents
│   └── scripts/                    # Backend verification, data generation scripts
├── frontend/                       # React 19 Frontend Web Client
│   ├── src/
│   │   ├── app/                    # Providers, routers, styles entrypoints
│   │   ├── components/             # Reusable UI layouts (Sidebar, Footer, Toolbar)
│   │   ├── constants/              # Navigation endpoints & routes
│   │   ├── design-system/          # Custom atomic controls, charts, timeline
│   │   ├── features/               # Core UI page modules
│   │   │   ├── admin/              # Diagnostics Dashboard
│   │   │   ├── ai-scientist/       # AI Scientist panel, Experiment panel
│   │   │   ├── digital-twin/       # 3D Solar Twin, Canvas, active regions
│   │   │   ├── knowledge-graph/    # React Flow network, Inspector
│   │   │   ├── mission/            # Overview, Operations, and Replay UI
│   │   │   └── physics/            # Wavelet, PSD, thermal analysis charts
│   │   ├── hooks/                  # WebSocket listener hooks & Query hooks
│   │   └── services/               # REST API fetchers
├── shared/                         # Shared model schemas & type definitions
├── docker/                         # Empty folder reserved for container configs
├── docs/                           # Legacy architectural documentation
└── scripts/                        # Monorepo validation scripts (SIT verification)
```

---

## 📂 Detailed Folder Index

### 1. `/backend`
*   **Purpose**: The central processing layer of the platform.
*   **Owner Module**: API Gateway / Backend Team.
*   **Dependencies**: `python-dotenv`, `fastapi`, `uvicorn`, `torch`, `numpy`, `pandas`, `xgboost`, `websockets`, `langchain`.
*   **How it connects**: Runs the REST and WebSocket servers, which the frontend connects to for all data points.

### 2. `/backend/aditya_flare`
*   **Purpose**: Houses the neural networks, XGBoost nowcasting algorithms, conformal boundary estimators, and decision thresholds.
*   **Owner Module**: AI Research & Prediction team.
*   **Dependencies**: PyTorch, Scikit-learn, joblib.
*   **How it connects**: Ingested by the API gateway to compute predictions on-the-fly and save outputs to the database.

### 3. `/backend/physics_engine`
*   **Purpose**: Performs mathematical physics transformations on soft/hard X-ray counts.
*   **Owner Module**: Solar Physics team.
*   **Dependencies**: Scipy, PyWavelets, SymPy.
*   **How it connects**: Processes raw telemetry from the Event Bus, producing feature vectors consumed by both the AI forecasting models and the UI charts.

### 4. `/backend/reasoning`
*   **Purpose**: Manages the LangGraph agent state machine representing the AI Scientist.
*   **Owner Module**: AI Agents / SRE team.
*   **Dependencies**: LangChain, LangGraph, OpenAI/Anthropic/Gemini SDKs.
*   **How it connects**: Triggered via `POST /api/reasoning/analyze` to fetch real-time state, query the KG, and stream Markdown reasoning outputs.

### 5. `/frontend`
*   **Purpose**: The web dashboard interface.
*   **Owner Module**: Frontend Team.
*   **Dependencies**: `react`, `react-router-dom`, `zustand`, `@tanstack/react-query`, `three`, `@react-three/fiber`, `@xyflow/react` (React Flow), `plotly.js-dist-min`.
*   **How it connects**: Fetches telemetry via REST, listens to WS updates from `ws://localhost:8000/ws/live`, and presents visual panels to the user.

### 6. `/shared`
*   **Purpose**: Shared data contracts (JSON/TS schemas).
*   **Owner Module**: Systems Integration.
*   **Dependencies**: None.
*   **How it connects**: Declares standard telemetry payloads and event names, preventing contract drift between React frontend and FastAPI backend.
