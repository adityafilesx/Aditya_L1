# 04. Backend Documentation

This document describes the design, class layouts, functions, workflows, and performance profiles of the backend Python application.

---

## 🚪 API Gateway & Main Entry (`backend/api/main.py`)

### Purpose
The entry point for the FastAPI server. It mounts all routers, configures Middlewares (including CORS), and runs the startup/shutdown hooks that start the telemetry simulators and background workers.

### Dependencies
`fastapi`, `uvicorn`, `api.routes`, `api.ws.live`, `api.state`.

### Key Code Patterns
*   **Application Startup**: Starts the background thread generator `generator.start()` (defined in `events/generator.py`).
*   **State Management**: Registers `AppState` dynamically so all routes can access running objects.

---

## ⚙️ App State (`backend/api/state.py`)

### Purpose
Acts as the central, thread-safe in-memory cache for all engine instances.

### Key Class: `AppState`
```python
class AppState:
    def __init__(self):
        self.latest_telemetry = None
        self.latest_physics = None
        self.latest_forecast = None
        self.latest_decision = None
        self.knowledge_graph = None
        self.reasoning_engine = None
```
This state is referenced throughout the application lifecycle to query telemetry history, active region counts, and model latencies.

---

## 📡 Live Stream WebSocket (`backend/api/ws/live.py`)

### Purpose
Provides a single high-performance connection pool where clients receive live-updates.

### Key Workflows
*   **Subscription Loop**: Upon connection, the client is subscribed to seven channels: `telemetry`, `physics`, `forecast`, `digital_twin`, `system`, `alerts`, and `mission_state`.
*   **Task Forwarding**: Uses `asyncio.create_task` to run parallel, non-blocking loops forwarding events from the `MissionBus` to the WebSocket connection.

---

## 📊 Feature Pipeline & Physics Extraction (`backend/physics_engine/`)

### 1. Feature Pipeline (`physics_engine/feature_pipeline.py`)
*   **Purpose**: Orchestrates the raw telemetry transformations.
*   **Input**: Raw telemetry dictionary (containing `goes_xrs_b`, `solexs_sdd2_ctr`).
*   **Output**: Unified feature vector (NumPy array).
*   **Method**: Combines Wavelet power spectral density (PSD), Neupert scores, and thermodynamic temperature estimates.

### 2. Thermodynamics Engine (`physics_engine/thermodynamics.py`)
*   **Purpose**: Computes flare temperature and emission measure from soft X-ray ratios.
*   **Inputs**: `goes_xrs_a` (short band) and `goes_xrs_b` (long band).
*   **Outputs**: `electron_temperature_mk` (Million Kelvin) and `emission_measure`.
*   **Formulas**:
    $$T = \frac{A}{\ln(Flux_B / Flux_A)}$$

### 3. Wavelets Engine (`physics_engine/wavelets.py`)
*   **Purpose**: Decomposes count-rate sequences into time-frequency spaces.
*   **Algorithms**: Continuous Wavelet Transform (CWT) using the Morlet wavelet.

---

## 🧠 SRE (Scientific Reasoning Engine) (`backend/reasoning/`)

### 1. Reasoner Agent (`reasoning/reasoner.py`)
*   **Purpose**: Evaluates prompts using semantic context matrices.
*   **Workflows**:
    1. Receives prompt query (e.g. "Explain today's flare").
    2. Calls `context_builder.py` to extract active region locations, Neupert curves, and ensemble prediction values.
    3. Prompts LLM using a structured markdown format requesting LaTeX-compatible scientific analysis.

### 2. Context Builder (`reasoning/context_builder.py`)
*   **Purpose**: Assembles real-time platform states into an XML/JSON context block.
*   **Output**: Context string containing:
    *   Active solar status (e.g., active regions, flare levels).
    *   Predictions from TCN/Transformer ensemble.
    *   System health metrics (CPU, Memory, WS connection pool sizes).
