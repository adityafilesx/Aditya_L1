# Complete Feature Matrix — Aditya-L1 Space Weather Platform

This document catalogs every functional feature of the platform, detailing its purpose, technical implementation, dependencies, outputs, and planned enhancements.

---

## 1. Telemetry & Ingestion Subsystems

### 1.1 Cadence Resampler & Aligner
*   **Purpose:** Standardize diverse telemetry streams onto a uniform timeline for model inputs.
*   **Implementation:** Reads raw telemetry files (e.g. Parquet or CSV) and interpolates them onto a 1-minute time index using forward-fill and linear methods.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `pandas`, `numpy`, `aditya_flare.models.dataset`.
*   **Outputs:** Synchronized DataFrame containing aligned instrument values.
*   **Future Work:** Add custom interpolation models for periods with high telemetry gap frequencies.

### 1.2 Telemetry Ingestion Health Monitor
*   **Purpose:** Track system errors, missing frames, and data transmission issues.
*   **Implementation:** Analyzes packet headers to count missing frames, calculate latency, and flag dropouts.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `aditya_flare.decision.telemetry_health`.
*   **Outputs:** Packet loss metrics, data rate statistics, and warning flags.
*   **Future Work:** Connect warning flags to the operational state machine to trigger system fallback modes.

---

## 2. Calibration Subsystems

### 2.1 Photon-to-Flux Conformal Calibration
*   **Purpose:** Calibrate raw photon count readings to standard physical flux values.
*   **Implementation:** Converts raw instrument rates (e.g. from SoLEXS) into physical reference flux units ($W/m^2$ equivalent to GOES).
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `scripts/fit_conformal_calibration.py`, `aditya_flare.calibration`.
*   **Outputs:** Calibrated flux value and confidence intervals.
*   **Future Work:** Implement dynamic calibration updates that adapt to solar cycle variations.

---

## 3. Feature Engineering Subsystems

### 3.1 Time-Series Derivative & Trend Extraction
*   **Purpose:** Calculate rates of change and acceleration across telemetry channels.
*   **Implementation:** Computes rolling slope and acceleration metrics over multiple window sizes (e.g. 5, 15, and 30 minutes).
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `pandas`, `scipy.signal`.
*   **Outputs:** Rolling derivative and trend arrays.
*   **Future Work:** Optimize window sizes based on real-time solar wind speed inputs.

---

## 4. Physics Diagnostics Subsystems

### 4.1 Neupert Derivative Analyzer
*   **Purpose:** Assess coronal heating from impulsive electron acceleration.
*   **Implementation:** Calculates the correlation coefficient between the hard X-ray flux and the soft X-ray derivative:
    $$ r = \text{corr}(F_{hard}, \frac{dF_{soft}}{dt}) $$
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `physics_engine/neupert.py`, `scipy.stats`.
*   **Outputs:** Neupert effect correlation scores.
*   **Future Work:** Implement dynamic time-lag offsets to improve correlation accuracy.

### 4.2 Wavelet Spectrogram Analytics
*   **Purpose:** Detect localized transient bursts and solar microflares.
*   **Implementation:** Applies Continuous Wavelet Transforms (CWT) using Complex Morlet wavelets and Discrete Wavelet Transforms (DWT) for high-frequency coefficient extraction.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `physics_engine/wavelets.py`, `pywt`.
*   **Outputs:** Wavelet scalogram values.
*   **Future Work:** Accelerate transform speeds using GPU-based PyWavelets.

### 4.3 Power Spectral Density (PSD) Analysis
*   **Purpose:** Identify dominant frequencies and microburst patterns.
*   **Implementation:** Applies Fast Fourier Transforms (FFT) to extract spectral peaks and assess spectral flatness.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `physics_engine/spectral.py`, `scipy.signal`.
*   **Outputs:** Dominant spectral frequencies and PSD plots.
*   **Future Work:** Set up alerts for specific spectral peaks linked to pre-flare oscillations.

### 4.4 Coronal Entropy Diagnostics
*   **Purpose:** Measure complexity shifts and stability in telemetry streams.
*   **Implementation:** Computes Shannon entropy and spectral complexity scores over moving windows.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `physics_engine/entropy.py`.
*   **Outputs:** Time-series complexity metrics.
*   **Future Work:** Compare entropy trends across multiple active regions to improve predictions.

---

## 5. Forecasting & AI Subsystems

### 5.1 Deep Learning Sequence Forecasting (TCN & Transformer)
*   **Purpose:** Predict flare probabilities over horizons ranging from 15 to 60 minutes.
*   **Implementation:** Employs Temporal Convolutional Networks (TCN) for temporal feature mapping and Transformer models for sequence attention.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** PyTorch, `aditya_flare.ai_engine.models`.
*   **Outputs:** Dynamic forecast probabilities and uncertainty bounds.
*   **Future Work:** Export models to ONNX to lower operational runtime latency.

### 5.2 XGBoost & LightGBM Nowcasting
*   **Purpose:** Provide fast predictions for real-time trigger assessments.
*   **Implementation:** Trains gradient-boosted decision trees using aligned telemetry and derivative features.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `xgboost`, `lightgbm`, `scripts/predict_nowcast.py`.
*   **Outputs:** Binary classification indicating flare risk.
*   **Future Work:** Integrate directly into the flight system's telemetry processing loop.

### 5.3 SHAP Explainability Integration
*   **Purpose:** Provide physical explanations for model forecast outputs.
*   **Implementation:** Computes SHAP feature importance values to show the impact of individual features on forecasts.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `shap`, `matplotlib`, `aditya_flare.ai_engine.explainability`.
*   **Outputs:** SHAP summary plots and horizontal waterfall charts.
*   **Future Work:** Expose SHAP results via FastAPI endpoints for the frontend dashboard.

---

## 6. Mission Operations & Decision Engine

### 6.1 Operational State Machine
*   **Purpose:** Manage spacecraft alert states based on flare risk.
*   **Implementation:** Transitions spacecraft state (`NOMINAL` -> `WATCH` -> `ALERT` -> `DECAY` -> `RECOVERY`) using flare probabilities and physics-based thresholds.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `aditya_flare.decision.state_machine`.
*   **Outputs:** Spacecraft alert state and transition logs.
*   **Future Work:** Add an override mode allowing operators to manually force state transitions.

### 6.2 Recommendation Engine
*   **Purpose:** Provide actionable recommendations for spacecraft operators.
*   **Implementation:** Generates plain-text descriptions and command actions based on current alert states and active alarms.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `aditya_flare.decision.recommendation`.
*   **Outputs:** Action briefs and scientific justifications.
*   **Future Work:** Build automated email and SMS notification loops for high-severity alerts.

### 6.3 Drift Monitor
*   **Purpose:** Identify sensor degradation and data distribution shifts.
*   **Implementation:** Uses Kolmogorov-Smirnov statistical tests to compare live telemetry distributions against baseline configurations.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `aditya_flare.decision.drift_monitor`.
*   **Outputs:** Drift metrics and system warnings.
*   **Future Work:** Connect drift alarms to automatically trigger model retraining runs.

---

## 7. Multi-Modal Digital Twin & Knowledge Graph

### 7.1 Active Region Digital Twin
*   **Purpose:** Match active regions to physical evolution benchmarks.
*   **Implementation:** Evaluates similarity scores and complexity metrics across solar region templates.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `aditya_flare.multi_modal.digital_twin.state_tracker`.
*   **Outputs:** Similarity index and stage classifications.
*   **Future Work:** Integrate with SDO/AIA vision embeddings to improve structural similarity checks.

### 7.2 Relational Event Graph
*   **Purpose:** Map causal connections between solar events and spacecraft alerts.
*   **Implementation:** Builds a relational network linking active regions, flare events, and alert triggers.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `aditya_flare.multi_modal.knowledge_graph.event_graph`, `networkx`.
*   **Outputs:** NetworkX relationship structures.
*   **Future Work:** Connect the graph backend to SQLite for persistence across restarts.

---

## 8. Visualization, Research, & Deployment

### 8.1 Scientific Visualization Suite
*   **Purpose:** Generate detailed reports and plots for post-event analysis.
*   **Implementation:** Produces custom spectral plots, confidence intervals, and SHAP diagrams.
*   **Current Status:** ✅ Fully Implemented.
*   **Dependencies:** `matplotlib`, `plotly`, `aditya_flare.visualization`.
*   **Outputs:** Saved PNG images and PDF summary reports.
*   **Future Work:** Support rendering visualizations as interactive elements in web interfaces.

### 8.2 Deployment & REST APIs
*   **Purpose:** Expose platform services to external clients and dashboards.
*   **Implementation:** Exposes core functionality as local Python APIs.
*   **Current Status:** 🔴 Missing.
*   **Dependencies:** FastAPI, Uvicorn (Planned).
*   **Outputs:** HTTP endpoints and JSON data formats.
*   **Future Work:** Implement FastAPI wrappers and WebSocket streams in the upcoming phase.
