# Operations Center Architecture

## Overview
The Operations Center is designed to support deep investigative workflows for the Aditya-L1 mission. It abandons the standard dashboard model in favor of a strict operational progression.

## Workflow Phases
The UI is grouped into four distinct phases, driven by a global `Event Context` stored in `st.session_state`.

### 1. Monitor
* **Header**: Toggles between LIVE mode and DEMO mode.
* **Flight Recorder**: Controls time. Operators can pause, step, or jump to historical flares.
* **Telemetry**: High-resolution, multi-panel Plotly chart synchronizing SoLEXS flux, HEL1OS flux, Hardness Ratio, and AI Forecast probabilities along a unified X-axis.

### 2. Investigate (Event Inspector)
When telemetry crosses a threshold, operators use the Event Inspector tabs:
* **Physics Diagnostics**: Deep dive into Power Spectral Density (PSD), Wavelet Scalograms, and T vs EM hysteresis.
* **AI Explainability**: Inspects SHAP values and Feature Importances for the current model prediction.
* **Model Comparison**: Real-time evaluation of XGBoost, TCN, and Transformer metrics (TSS, FAR, Latency).
* **Sensor Inspector**: Advanced telemetry health, showing packet loss, drift, and noise levels.

### 3. Respond
* **Decision Engine**: Generates mission-critical recommendations (e.g., "Prepare Burst Mode") and clearly explains *why* the recommendation was made.
* **Alert Management**: A filterable, priority-ranked list of notifications from all subsystems.

### 4. Review
* **Mission Timeline**: A chronological log mapping AI triggers, Physics anomalies, and Mission decisions.
* **Operator Notebook**: Allows users to manually annotate events. These annotations persist in the session state.

## State Management (`ui/state.py`)
Because Streamlit re-runs on every interaction, `ui/state.py` maintains:
* `op_mode` (LIVE/DEMO)
* `event_context` (Selected Time Window)
* `flight_recorder` (Playback speed and state)
* `operator_notebook` (In-memory log)

## Services
The `ui/services/` layer dynamically responds to the `Event Context`. If in DEMO mode and looking at a historical flare, the mock services return the exact sequence of events for that timeframe, simulating a true Flight Recorder experience.
