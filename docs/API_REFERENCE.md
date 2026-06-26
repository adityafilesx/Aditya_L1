# API Reference Manual — Aditya-L1 Platform

This document describes the API methods, parameters, and payloads for the Aditya-L1 Space Weather Intelligence Platform.

---

## 1. Core API Endpoints

### 1.1 Telemetry APIs

#### `aditya_flare.models.dataset.load_aligned_telemetry`
*   **Purpose:** Load resampled and synchronized telemetry streams.
*   **Method:** In-Process Python API.
*   **Input Parameters:**
    *   `filepaths`: list of paths to raw Parquet/CSV data files.
    *   `resample_cadence`: string (default `'1min'`).
*   **Response Payload:**
    *   `pandas.DataFrame` containing aligned and interpolated instrument channels (`solexs_flux`, `hel1os_counts`, `suit_uv`).

### 1.2 Physics APIs

#### `physics_engine.feature_pipeline.compute_all_features`
*   **Purpose:** Extract physics features and spectral diagnostics from telemetry streams.
*   **Method:** In-Process Python API.
*   **Input Parameters:**
    *   `telemetry_window`: `pandas.DataFrame` (min. 60-minute window).
*   **Response Payload:**
    ```python
    {
        "neupert_correlation": 0.82,
        "wavelet_burst_detected": False,
        "psd_peak_frequency": 0.0033,
        "psd_peak_power": 48.2,
        "spectral_entropy": 0.38,
        "temperature_estimate": 14.2,
        "emission_measure_estimate": 1.2e48
    }
    ```

### 1.3 Forecasting & AI APIs

#### `aditya_flare.ai_engine.predict.get_ensemble_forecast`
*   **Purpose:** Calculate flare probabilities using forest and deep sequence models.
*   **Method:** In-Process Python API.
*   **Input Parameters:**
    *   `feature_matrix`: `numpy.ndarray` containing aligned time-series features.
    *   `models`: list of strings (e.g. `['XGBoost', 'TCN', 'Transformer']`).
*   **Response Payload:**
    ```python
    {
        "consensus_probability": 0.208,
        "uncertainty_lower": 0.18,
        "uncertainty_upper": 0.23,
        "individual_predictions": {
            "XGBoost": 0.19,
            "TCN": 0.21,
            "Transformer": 0.22
        }
    }
    ```

### 1.4 Mission & Decision Support APIs

#### `aditya_flare.decision.state_machine.update_state`
*   **Purpose:** Evaluate operational state machine transitions.
*   **Method:** In-Process Python API.
*   **Input Parameters:**
    *   `flare_probability`: float.
    *   `physics_indicators`: dict (output from Physics API).
*   **Response Payload:**
    ```python
    {
        "current_state": "WATCH",
        "previous_state": "NOMINAL",
        "alert_level": "PRE_ALERT",
        "state_change_timestamp": "2026-06-25T18:00:00Z"
    }
    ```

#### `aditya_flare.decision.recommendation.get_recommendation`
*   **Purpose:** Generate operational recommendations for spacecraft operators.
*   **Method:** In-Process Python API.
*   **Input Parameters:**
    *   `current_state`: string.
    *   `telemetry_health`: dict.
*   **Response Payload:**
    ```python
    {
        "recommendation": "Prepare Spacecraft Burst Mode",
        "confidence": "HIGH",
        "scientific_rationale": "Ensemble probability exceeds 20.8% threshold. Neupert derivative shows rapid pre-flare thermal heating.",
        "required_action": "Enable high-cadence payload acquisition loop"
    }
    ```

---

## 2. Missing APIs Required by the Future Frontend

To support the upcoming HTML5/CSS/JS dashboard, these local Python APIs must be wrapped in REST endpoints (using FastAPI) and WebSocket routers:

1.  **`/api/telemetry/stream` (GET):** WebSockets/Long-Polling endpoint exposing aligned telemetry data for real-time charts.
2.  **`/api/physics/diagnostics` (POST):** REST endpoint exposing spectral and wavelet diagnostic features for the Event Inspector.
3.  **`/api/decision/status` (GET):** REST endpoint exposing active alert levels, state machine states, and operator recommendations.
4.  **`/api/digital-twin/region` (GET):** REST endpoint exposing active region similarities and twin model structures.
5.  **`/api/explainability/shap` (GET):** REST endpoint exposing SHAP waterfall chart values for the selected prediction.
6.  **`/api/health/drift` (GET):** REST endpoint exposing KS-statistic drift values and payload packet drop statistics.
