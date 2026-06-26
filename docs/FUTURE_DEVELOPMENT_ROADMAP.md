# Future Development Roadmap — Aditya-L1 Platform

This document presents the consolidated development roadmap, comparing implemented components with future tasks and detailing the milestones, deliverables, and acceptance criteria.

---

## 1. Feature Progress Summary

| Segment | Feature Name | Status | Target File/Package |
| :--- | :--- | :--- | :--- |
| **Backend** | 1-Min Telemetry Resampler | ✅ Complete | `aditya_flare/models/dataset.py` |
| **Backend** | Ingest Health Monitor | ✅ Complete | `aditya_flare/decision/telemetry_health.py` |
| **Physics** | Neupert Effect Correlation | ✅ Complete | `physics_engine/neupert.py` |
| **Physics** | Wavelet Spectrograms | ✅ Complete | `physics_engine/wavelets.py` |
| **Physics** | Spectral Power Density | ✅ Complete | `physics_engine/spectral.py` |
| **Physics** | Coronal Entropy Diagnostics | ✅ Complete | `physics_engine/entropy.py` |
| **AI/ML** | Fast nowcast XGBoost/LGBM | ✅ Complete | `scripts/predict_nowcast.py` |
| **AI/ML** | Deep Sequence models (TCN/Transformer) | ✅ Complete | `aditya_flare/ai_engine/models/` |
| **AI/ML** | SHAP Explainability plots | ✅ Complete | `aditya_flare/ai_engine/explainability.py` |
| **AI/ML** | Auto-retraining on drift | 🟡 Partial | `aditya_flare/decision/drift_monitor.py` |
| **Operations**| Spacecraft State Machine | ✅ Complete | `aditya_flare/decision/state_machine.py` |
| **Operations**| Operator Recommendations | ✅ Complete | `aditya_flare/decision/recommendation.py` |
| **Twin & Graph**| Solar Active Region Twin | ✅ Complete | `aditya_flare/multi_modal/digital_twin/` |
| **Twin & Graph**| Relational Event Graph | 🟡 Partial | `aditya_flare/multi_modal/knowledge_graph/` |
| **Frontend** | HTML5/CSS/JS Console | 🔴 Missing | Planned (Phase 6) |
| **Deployment** | REST APIs / WebSockets | 🔴 Missing | Planned (Phase 6) |
| **Deployment** | Docker Deployment Files | 🔴 Missing | Planned (Phase 6) |

---

## 2. Master Development Roadmap (Phases 6–7)

### Phase 6: REST API Layer & Web Interface

#### Module 6.1: FastAPI REST Wrapper
*   **Deliverable:** FastAPI web server exposing telemetry streams, recommendations, SHAP values, and state machine transitions.
*   **Dependencies:** `aditya_flare.ai_engine.predict`, `physics_engine.feature_pipeline`.
*   **Milestone:** All local Python functions wrapped in HTTP endpoints.
*   **Acceptance Criteria:** FastAPI `/docs` displays endpoints with complete JSON schemas.

#### Module 6.2: WebSocket Live Stream Router
*   **Deliverable:** WebSocket route streaming telemetry updates, alerts, and drift warnings to clients.
*   **Dependencies:** `aditya_flare.decision.state_machine`, `aditya_flare.decision.drift_monitor`.
*   **Milestone:** Live streaming of spacecraft alert events to clients.
*   **Acceptance Criteria:** Clients connect to `ws://` and receive event JSON payloads.

#### Module 6.3: HTML5/CSS/JS Operations Console
*   **Deliverable:** Responsive HTML5 dashboard displaying metrics, synchronized charts, event timelines, and operator notebooks.
*   **Dependencies:** UI design guidelines, FastAPI REST/WebSocket APIs.
*   **Milestone:** Launch of the interactive dashboard interface.
*   **Acceptance Criteria:** The interface connects to endpoints, plots telemetry streams, updates alert states, and runs in standard browsers.

---

### Phase 7: Production Orchestration & Scientific Expansion

#### Module 7.1: Containerized Deployment
*   **Deliverable:** Docker configuration files compiling Heasoft, Xspec, python-venv, and the API web service.
*   **Dependencies:** Complete project source files.
*   **Milestone:** Multi-stage Docker image builds.
*   **Acceptance Criteria:** Running the container spins up the API and serves the frontend dashboard.

#### Module 7.2: Persistent Knowledge Graph
*   **Deliverable:** SQLite-backed graph database to store active region relationships across system restarts.
*   **Dependencies:** `aditya_flare.multi_modal.knowledge_graph.event_graph`.
*   **Milestone:** Relational node updates persisted to disk.
*   **Acceptance Criteria:** Restarting the process preserves active region relationships.
