# Master Technical Specification — Aditya-L1 Space Weather Intelligence Platform

This document serves as the master technical specification and consolidated baseline for the Aditya-L1 Space Weather Intelligence Platform, providing the definitive reference for the platform's core operational objectives, scientific standards, and system maturity.

---

## 1. Platform Overview

### 1.1 Purpose & Scope
The Aditya-L1 Space Weather Intelligence Platform is an integrated ground-and-space software suite designed to ingest, calibrate, analyze, and forecast telemetry data from the Aditya-L1 solar observation spacecraft. The platform acts as the mission's primary real-time operational monitor and predictive alert engine, providing automated warnings of solar flare events to protect spacecraft payloads and terrestrial power/communication grids.

### 1.2 Scientific Objectives
1.  **Multi-Modal Solar Flare Forecasting:** Correlate soft X-ray fluxes (from SoLEXS) and hard X-ray counts (from HEL1OS) to predict the occurrence, peak time, and intensity class (A, B, C, M, X class) of solar flares.
2.  **Physics-Informed Diagnostics:** Implement signal analysis techniques that capture physical solar thermodynamics:
    *   *Neupert Effect Correlation:* Measure coronal heating from impulsive electron acceleration by correlating soft X-ray derivatives with hard X-ray fluxes.
    *   *Spectral Scaling & Wavelets:* Isolate micro-flares and transient microburst oscillations using Continuous Wavelet Transforms (CWT) and Discrete Wavelet Transforms (DWT).
    *   *Thermodynamic Parameter Fallbacks:* Estimate coronal plasma temperatures ($T$) and emission measures ($EM$) without full spectral inversion using empirical hardness ratio ($HR$) scaling.

### 1.3 Operational Objectives
1.  **Low-Latency Command State Transitions:** Trigger spacecraft safety overrides (e.g., transitioning from `NOMINAL` to `WATCH` or `ALERT` modes and auto-adjusting instrument attenuators) under strict sub-millisecond execution constraints.
2.  **Telemetry Health & Drift Management:** Ingest and resample raw telemetry streams down to a standardized 1-minute cadence, monitoring packet dropouts and sensor drift via Kolmogorov-Smirnov statistical tests.
3.  **Explainable Action Directives:** Deliver structured recommendations to flight controllers (e.g., payload high-cadence burst activations) backed by SHAP explainability feature bars.

### 1.4 Target Users
*   **ISRO Spacecraft Operators / Flight Directors:** Rely on the high-level status monitors, decision engines, and alert tickers to issue payload commands.
*   **Space Weather Researchers & Solar Physicists:** Analyze spectral density peaks, wavelet coefficients, and temperature/emission measure curves.
*   **Subsystem Engineers:** Track packet drop rates, sensor drift warnings, and instrument calibration curves.

---

## 2. Inconsistency Resolution

During the baseline audit, a few discrepancies between planned designs and the actual codebase were identified and resolved:

### 2.1 UI Presentation Layer (Streamlit Removal)
*   *Inconsistency:* Older documentation (`user_guide.md`, `DESIGN_SYSTEM.md`) references launching a Streamlit dashboard directly.
*   *Resolution:* The legacy Streamlit frontend (`ui/`) has been officially removed. All user interfaces are being replaced by an HTML5/CSS/JavaScript console. The backend engine (`aditya_flare`) has zero remaining runtime dependencies on Streamlit, as confirmed by successful test executions.

### 2.2 Local Developer Path Overrides
*   *Inconsistency:* Several production-bound scripts contain absolute user folder paths (`/Users/aditya1981/...`) and specific conversation IDs.
*   *Resolution:* These paths are categorized as critical technical debt (see `TECHNICAL_DEBT_MASTER.md`). In the future roadmap, all dynamic paths must be loaded from `aditya_flare/config/settings.yaml` or resolved dynamically at runtime using `pathlib.Path`.

### 2.3 API Boundaries
*   *Inconsistency:* Prior documents call the interfaces "APIs" but implement them as in-process local Python function calls.
*   *Resolution:* The new specification defines these interfaces as the exact contract templates to be wrapped in FastAPI REST endpoints and WebSocket routers in the upcoming Phase 6.
