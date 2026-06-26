# 20. Complete Feature Matrix

This document provides a matrix mapping every system capability to its respective backend modules, API routes, frontend layout pages, and execution statuses.

---

## 🗂️ Master Feature Matrix

| Feature | Primary Goal | Backend Module | Frontend Component / Page | Connected API Endpoint | Engine Under the Hood | Current Status | Major Dependencies | Future Expansion |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Real-time Ingestion & Streaming** | Deliver sub-second counts to UI | `events/generator.py` | `useStreamStore.ts` | WebSocket `/ws/live` | Telemetry & Streaming Engine | **PRODUCTION READY** | `websockets`, `asyncio` | Transition to Apache Kafka broker |
| **Multi-Horizon Forecasting** | Predict flares 15m to 6h ahead | `aditya_flare/models/forecaster.py` | `/overview` Forecast cards | `GET /api/forecast/horizons` | AI Forecast Engine | **PRODUCTION READY** | PyTorch, `joblib`, Scikit-learn | Graph Neural Networks (GNNs) |
| **Thermodynamic Spectral Fits** | Calculate temperature and emission measure | `physics_engine/thermodynamics.py` | `/investigation/physics` DEM chart | `GET /api/physics/summary` | Physics Engine | **PRODUCTION READY** | SciPy, `numpy` | Non-thermal emission fit integration |
| **Wavelet Power Analysis** | Time-frequency counts decomposition | `physics_engine/wavelets.py` | `/investigation/physics` Spectrogram | `GET /api/physics/summary` | Physics Engine | **PRODUCTION READY** | `PyWavelets` | Real-time CWT spectrogram zooming |
| **Solar Digital Twin** | Interactive 3D sun visualizer | `api/routes/digital_twin.py` | `/digital-twin` TwinCanvas | `GET /api/digital-twin/state` | Digital Twin Engine | **PRODUCTION READY** | Three.js, React Three Fiber | Real-time SDO image texture mapping |
| **Knowledge Graph Explorer** | Map active region connections | `api/routes/knowledge_graph.py` | `/knowledge/graph` | `GET /api/knowledge-graph/` | Knowledge Graph Engine | **PRODUCTION READY** | React Flow, D3-Force | GraphRAG with vector indices |
| **Scientific Reasoning Workspace** | Agent chat interface for state analysis | `reasoning/reasoner.py` | `/research` Conversation panel | `POST /api/reasoning/analyze` | Scientific Reasoning Engine | **PRODUCTION READY** | LangGraph, LangChain | Full integration of local LLM models |
| **Historical Replay** | Scrub and replay flare timelines | `api/routes/timeline.py` | `/operations` Replay controller | `GET /api/operations/timeline` | Telemetry Engine | **PRODUCTION READY** | Pandas, Parquet datasets | Automated report compilation on load |
| **System Diagnostics** | Real-time sub-engine health checker | `api/routes/system.py` | `/system/admin` Diagnostics card | `GET /api/system/diagnostics` | System Health Engine | **PRODUCTION READY** | `psutil`, FastAPI state | Prometheus & Grafana integrations |
