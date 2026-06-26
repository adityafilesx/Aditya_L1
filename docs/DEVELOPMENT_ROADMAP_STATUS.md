# Development Roadmap Status — Aditya-L1 Platform

This document maps the planned milestones and feature objectives of the Aditya-L1 Space Weather Intelligence Platform against the actual implemented codebase.

---

## 1. Feature Map & Verification Status

### 1.1 Telemetry & Ingestion Pipeline
*   **✅ Fully Implemented:**
    *   **Resampler & Aligner:** Standardizes multi-instrument timelines (SoLEXS, HEL1OS, external GOES) onto a clean 1-minute cadence.
    *   **Calibration Engine:** Maps raw photon readings into physical scale ranges.
    *   **Gaps & Packet Health Ingest:** Detects missing packets and signal dropouts.
*   **🟡 Partially Implemented:**
    *   **Automatic SUIT Image Alignment:** SUIT UV image metadata reads are functional, but automatic solar disk centering lacks geometric validation tests.

### 1.2 Physics Engine
*   **✅ Fully Implemented:**
    *   **Thermal Diagnostic Derivatives:** Neupert effect ratios mapped across hard/soft X-ray sensors.
    *   **PSD Spectral peak matching:** FFT power analyses to catch microbursts.
    *   **Scalogram transforms:** Wavelet filters for transient localized heating bounds.
    *   **Thermodynamic diagnostics:** Entropy calculations to track coronal state shifts.

### 1.3 Machine Learning & Deep Forecast Models
*   **✅ Fully Implemented:**
    *   **Nowcast Classifiers:** Low-latency XGBoost and LightGBM engines.
    *   **Sequence Models:** Multi-task and Physics-Attention deep architectures (TCN, Transformer).
    *   **Explainability Matrices:** Global and local SHAP explanation engines.
*   **🟡 Partially Implemented:**
    *   **Real-time Model Retraining:** Scripts exist (`train.py`), but automatic pipeline triggers on performance drift alerts are not yet connected.

### 1.4 Mission Operations & Decision Support
*   **✅ Fully Implemented:**
    *   **State Machine:** Watch -> Alert -> Decay -> Recovery states are fully verified.
    *   **Recommendation Dispatcher:** Urgency ranking and action recommendations.
    *   **Drift Monitor:** Kolmogorov-Smirnov check routines mapping input feature deviations.

### 1.5 Multi-Modal Digital Twin & Knowledge Graph
*   **✅ Fully Implemented:**
    *   **Active Region Matcher:** Beta-Gamma-Delta magnetic class similarities.
    *   **Cross-Modal Attentional Layers:** Deep fusion layer mappings.
*   **🟡 Partially Implemented:**
    *   **Relational Link Crawler:** Spatial-temporal link crawls are supported locally via NetworkX but lack external graph server bindings.

### 1.6 Frontend presentation & Dashboards
*   **🔴 Missing:**
    *   **Interactive HTML/CSS/JS Panel:** Legacy Streamlit files were removed to prepare for a custom web console. Frontend client implementation is scheduled for the next development phase.

### 1.7 Deployment & Orchestration
*   **🟡 Partially Implemented:**
    *   **API Layer Execution:** API definitions exist as local python entry points. REST servers (e.g. FastAPI/Uvicorn) and WebSocket routes are designed but not yet written.
    *   **Docker Containerization:** Docker configurations are missing from the repository root.

---

## 2. Roadmap Progress Matrix

| Target Section | Objective Feature | Status | Target File / Module |
| :--- | :--- | :--- | :--- |
| **Telemetry** | 1-Min Cadence Resampler | ✅ Fully Implemented | `aditya_flare/models/dataset.py` |
| **Telemetry** | Ingest Health Monitor | ✅ Fully Implemented | `aditya_flare/decision/telemetry_health.py` |
| **Telemetry** | SUIT Disk Aligner | 🟡 Partially Implemented | `scripts/visualize_suit.py` |
| **Physics** | Neupert Derivative ($\frac{dF}{dt}$) | ✅ Fully Implemented | `physics_engine/neupert.py` |
| **Physics** | Wavelet Scalograms | ✅ Fully Implemented | `physics_engine/wavelets.py` |
| **Physics** | Power Spectral Density | ✅ Fully Implemented | `physics_engine/spectral.py` |
| **Physics** | Coronal Entropy Diagnostics | ✅ Fully Implemented | `physics_engine/entropy.py` |
| **AI Engine** | Nowcasting XGBoost/LGBM | ✅ Fully Implemented | `scripts/predict_nowcast.py` |
| **AI Engine** | DL TCN & Transformers | ✅ Fully Implemented | `aditya_flare/ai_engine/models/` |
| **AI Engine** | Explainability (SHAP) | ✅ Fully Implemented | `aditya_flare/ai_engine/explainability.py` |
| **AI Engine** | Drift-Triggered Retraining | 🟡 Partially Implemented | `aditya_flare/decision/drift_monitor.py` |
| **Operations** | Operational State Machine | ✅ Fully Implemented | `aditya_flare/decision/state_machine.py` |
| **Operations** | Action Recommendations | ✅ Fully Implemented | `aditya_flare/decision/recommendation.py` |
| **Twin & Graph**| Solar Active Region Twin | ✅ Fully Implemented | `aditya_flare/multi_modal/digital_twin/` |
| **Twin & Graph**| Relational Event Graph | 🟡 Partially Implemented | `aditya_flare/multi_modal/knowledge_graph/` |
| **Frontend** | HTML/CSS/JS Operations Desk | 🔴 Missing | Scheduled for Phase 6 |
| **Deployment** | REST APIs / WebSockets | 🔴 Missing | Scheduled for Phase 6 |
| **Deployment** | Docker / CI Pipelines | 🔴 Missing | Scheduled for Phase 6 |

---

## 3. Recommended Roadmap Execution Plan

1.  **Refactor Paths:** Standardize relative path structures across all Python scripts and C codebases.
2.  **API Wrapper Creation:** Build a FastAPI web server exposing `/api/telemetry/stream` and `/api/decision/status`.
3.  **Frontend Interface Development:** Build the HTML/CSS/JS workspace using components detailed in the Frontend Requirements report.
4.  **Dockerization:** Provide a uniform Docker image compiling Heasoft, Xspec, python-venv, and the API web service.
