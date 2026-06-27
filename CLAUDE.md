# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Aditya-L1 Mission Control — a real-time space-weather platform that ingests solar
telemetry (SoLEXS soft X-ray, HEL1OS hard X-ray, GOES XRS, proton flux), derives
physics parameters, runs ML flare forecasts, and streams everything over WebSockets
to a React Operations Center. Backend is FastAPI + asyncio; frontend is React 19 +
Vite + TypeScript.

## Critical: run from the repository root

Every backend module imports with the absolute `backend.` prefix (e.g.
`from backend.api.state import app_state`, `from backend.physics_engine...`). This
means **all Python commands — server, tests, scripts — must be run from the repo
root**, with the repo root on `PYTHONPATH`. The `cd backend && uvicorn api.main:app`
invocation shown in `README.md` does **not** work because `backend` is not importable
from inside `backend/`. Use the commands below instead.

A virtualenv already exists at the repo root: `.venv/` (Python 3.14).

## Common commands

```bash
# Activate the existing root venv
source .venv/bin/activate

# Run the API + WebSocket server (from repo root, note the backend. prefix)
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload

# Run all backend tests (from repo root)
python -m pytest backend/tests

# Run a single test file / test
python -m pytest backend/tests/test_physics_engine.py
python -m pytest backend/tests/test_physics_engine.py -k neupert -v

# Frontend dev server (proxies /api → :8000, WS → ws://localhost:8000/ws)
cd frontend && npm install && npm run dev      # http://localhost:5173

# Frontend build / lint
cd frontend && npm run build                   # tsc -b && vite build
cd frontend && npm run lint                    # eslint .
```

Dependencies: `backend/requirements-api.txt` is the minimal set to run the API
(FastAPI/uvicorn/websockets/psutil). `backend/requirements.txt` is the full ML/data
stack (XGBoost, torch, etc.) needed only for training/evaluation scripts and the
Streamlit nowcasting app (`backend/scripts/app.py`).

## Backend architecture

The system is event-driven around a single in-process pub/sub bus.

- **`backend/events/mission_bus.py`** — `MissionBus`, a global asyncio pub/sub bus.
  Producers `publish(channel, message)`; consumers `subscribe(channel)` to get an
  `asyncio.Queue`. Channels: `mission_state`, `telemetry`, `forecast`, `physics`,
  `digital_twin`, `system`, `alerts`.
- **`backend/events/generator.py`** — `MissionStateGenerator` (singleton `generator`).
  On `start()` it spawns one asyncio loop per data stream that mutates a shared
  `MissionState` and publishes to the bus at fixed cadences (telemetry 1s, physics 5s,
  etc.). This is the **simulation source** driving the live demo — flare escalation
  (NOMINAL=0 → WATCH=1 → ALERT=2) is modeled here. `MissionState` and all payload
  schemas live in `backend/events/models.py` (Pydantic).
- **`backend/api/state.py`** — `AppState` singleton (global `app_state`). Eagerly
  constructs the heavy engines once at startup and shares them across requests:
  `DecisionEngine`, `SolarDigitalTwin`, `EventKnowledgeGraph`,
  `MissionIntelligenceEngine`, `SpaceOnboardTrigger`. Also caches `latest_telemetry`,
  `latest_physics`, `latest_predictions`. AI model slots start as `None` and load
  lazily if artifacts are present.
- **`backend/api/main.py`** — FastAPI app. `lifespan` touches `app_state` (triggers
  engine init) and starts/stops `generator`. REST routers are under
  `backend/api/routes/*` mounted at `/api`; WebSocket routers under `backend/api/ws/*`
  mounted at `/ws`. CORS is fully open.
- **`backend/api/ws/live.py`** — the primary `/ws/live` endpoint. Per connection it
  spawns a forwarder task per channel that drains the bus queue and sends
  `{"type": CHANNEL_UPPER, "payload": ...}` JSON frames to the client.

Routes that have no live data fall back to **`backend/api/mock_data.py`** generators,
so endpoints return plausible payloads even before models/data are wired up.

### Reasoning engine (`backend/reasoning/`)

A separate multi-agent "Scientific Reasoner" pipeline, independent of the live stream:
`reasoner.py` (`ScientificReasoner`, the orchestrator) → `context_builder.py` →
`planner.py` → `router.py` → `agents/*` → `review_agent.py`, streamed to the frontend
via SSE. Agents (`physics`, `prediction`, `digital_twin`, `knowledge_graph`,
`mission`, `spectral`, `literature`, `experiment`, `report`, `review`) subclass
`agents/base_agent.py` and are registered on the router. `workflow.py` defines named
multi-step workflows (`flare_analysis`, `mission_briefing`, etc.) as ordered
`SubTask` sequences. Exposed through `backend/api/routes/reasoning.py`.

### Domain & ML packages

- **`backend/aditya_flare/`** — the core science library: `decision/` (state machine,
  adaptive thresholds, alerting), `calibration/` (conformal/GOES), `models/`
  (forecaster, onboard space trigger), `multi_modal/` (digital twin, knowledge graph,
  mission intelligence, SDO/SWIS/GOES fusion), `evaluation/`, `visualization/`.
- **`backend/physics_engine/`** — pure feature extractors (statistics, entropy,
  wavelets, spectral, thermodynamics, neupert, event segmentation) composed by
  `feature_pipeline.py`. These are the most heavily unit-tested modules.
- **`backend/ml/`** — the offline ML lifecycle: `training/`, `datasets/`, `labels/`,
  `calibration/`, `evaluation/`, `registry/`, `promotion/`, `serving/` (the
  `serving_apis.py` router mounted in `main.py`), `monitoring/`. Registry/dataset
  state is JSON under `backend/data/` (e.g. `ml_model_registry.json`).
- **`backend/scripts/`** — standalone CLIs for training, evaluation, data download,
  report generation, and daemons (`train_xgboost.py`, `evaluate_lead_time.py`,
  `run_operations_daemon.py`, `generate_master_catalog.py`, …). Run from repo root.

## Frontend architecture

- **`frontend/src/realtime/`** — the real-time core. `socket.ts` is a singleton
  `StreamingManager` that connects to `ws://localhost:8000/ws/live`, auto-reconnects,
  and dispatches frames by `type` into `streamStore.ts` (Zustand). High-frequency
  stream state lives in `streamStore`; UI/workspace state in `workspaceStore.ts`.
  WS base URL: `VITE_WS_BASE_URL` (default `ws://localhost:8000/ws`).
- **`frontend/src/api/`** — `client.ts` (`fetchClient`, `API_BASE_URL` from
  `VITE_API_BASE_URL`, default `http://localhost:8000/api`) and `endpoints.ts`.
  Server cache via `@tanstack/react-query`.
- **`frontend/src/app/`** — `routes.tsx` (lazy-loaded route tree under `<Layout>`),
  `providers.tsx`. Pages live in `frontend/src/features/*` (mission, forecast,
  physics, digital-twin, knowledge-graph, ai-scientist, research, investigation,
  admin). Shared UI in `design-system/` and `components/`.
- **Path aliases** (defined in both `vite.config.ts` and `tsconfig`): `@`, `@app`,
  `@components`, `@features`, `@hooks`, `@store`, `@services`, `@utils`,
  `@app-types`, `@constants`, `@styles`, `@assets`, `@design-system`. Use these
  rather than long relative paths. Vite dev server proxies `/api` to `:8000`.
- Visualization stack: Plotly.js (time series), Three.js / react-three-fiber (3D),
  @xyflow/react + elkjs (graphs), KaTeX (equations).

## Conventions

- Backend uses absolute imports rooted at `backend.` everywhere — keep this when
  adding modules, and always run tooling from the repo root.
- New live data: publish to a `MissionBus` channel in `generator.py`, add the channel
  to the list in `ws/live.py`, define the Pydantic payload in `events/models.py`,
  then handle the new `type` in the frontend `socket.ts` / `streamStore.ts`.
- New REST resource: add a router in `backend/api/routes/`, include it in
  `main.py` under the `/api` prefix; read shared engines via `app_state`, and provide
  a `mock_data.py` fallback if live data may be absent.
- `shared/` holds cross-cutting schema/type/constant definitions intended to stay in
  sync between backend and frontend.

## Notes / gotchas

- The live data shown by default is **simulated** by `generator.py`, not real
  telemetry. Real model/data wiring is gated on artifacts being present (AI model
  slots in `AppState` default to `None`).
- `data/` and `venv/` are git-ignored; large datasets and the per-developer venv are
  not committed.
- The repo root contains a number of ad-hoc analysis/scratch scripts
  (`scratch_*.py`, `fix_*.py`, `scan_frontend.py`, `test_*.py`) and generated `*.md`
  reports — these are one-off tools, not part of the application or its test suite.
