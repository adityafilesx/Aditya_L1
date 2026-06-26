# API Documentation — Aditya-L1 Space Weather Platform

This document describes the platform's backend API surfaces, detailing input, output, latency, and status.

---

## 1. Inference & Nowcast API

### Endpoint: `aditya_flare.ai_engine.predict`
*   **Method:** Python Interface / Local Call
*   **Input Parameters:**
    *   `features`: `dict` containing current aligned telemetry (e.g. `solexs_sdd2_ctr`, `goes_flux`, `suit_uv_mean`).
    *   `model_name`: `str` ("XGBoost", "LightGBM", "TCN", "Transformer", "Consensus").
*   **Output JSON Schema:**
    ```json
    {
      "model": "Consensus",
      "timestamp": "2026-06-25T12:20:00Z",
      "flare_probability": 0.208,
      "tss_score": 0.84,
      "uncertainty_range": [0.18, 0.23]
    }
    ```
*   **Dependencies:** `aditya_flare.ai_engine.registry`
*   **Latency:** ~5 ms (XGBoost) / ~28 ms (Transformer)
*   **Status:** ✅ Fully Implemented

---

## 2. Physics Diagnostics API

### Endpoint: `physics_engine.feature_pipeline`
*   **Method:** Python Interface / Local Call
*   **Input Parameters:**
    *   `time_series_data`: `pandas.DataFrame` containing X-ray flux history (min. 60-minute window).
*   **Output JSON Schema:**
    ```json
    {
      "neupert_derivative": 1.28e-5,
      "power_spectral_density_peak": 48.2,
      "wavelet_power_burst": false,
      "entropy_complexity": 0.42,
      "cooling_rate": -0.05
    }
    ```
*   **Dependencies:** `scipy.signal`, `numpy`
*   **Latency:** ~8 ms
*   **Status:** ✅ Fully Implemented

---

## 3. Space Trigger & State Machine API

### Endpoint: `aditya_flare.decision.state_machine`
*   **Method:** Python Interface / Local Call
*   **Input Parameters:**
    *   `flare_probability`: `float` (0.0 to 1.0)
    *   `physics_indicators`: `dict` (from Physics Diagnostics API)
    *   `telemetry_health`: `dict` (packet loss, drift metrics)
*   **Output JSON Schema:**
    ```json
    {
      "current_state": "WATCH",
      "previous_state": "NOMINAL",
      "alert_level": "PRE_ALERT",
      "last_state_change": "2026-06-25T12:14:00Z",
      "triggered_by": "model_ensemble_prob > 0.20"
    }
    ```
*   **Dependencies:** `aditya_flare.decision.alert_manager`
*   **Latency:** <1 ms
*   **Status:** ✅ Fully Implemented

---

## 4. Decision Engine & Recommendations API

### Endpoint: `aditya_flare.decision.recommendation`
*   **Method:** Python Interface / Local Call
*   **Input Parameters:**
    *   `state_data`: `dict` (from Space Trigger & State Machine API)
*   **Output JSON Schema:**
    ```json
    {
      "recommendation": "Prepare Spacecraft Burst Mode",
      "confidence": "HIGH",
      "scientific_rationale": "Ensemble probability exceeds 20.8% trigger. Neupert derivative shows rapid pre-flare thermal heating (+1.28e-5 W/m²/s). Telemetry quality is nominal (98%).",
      "required_action": "Enable high-cadence payload acquisition loop",
      "timestamp": "2026-06-25T12:20:00Z"
    }
    ```
*   **Dependencies:** `aditya_flare.decision.confidence`
*   **Latency:** ~2 ms
*   **Status:** ✅ Fully Implemented

---

## 5. Digital Twin & Active Region API

### Endpoint: `aditya_flare.multi_modal.digital_twin.state_tracker`
*   **Method:** Python Interface / Local Call
*   **Input Parameters:**
    *   `region_id`: `str` (e.g. "AR3684")
*   **Output JSON Schema:**
    ```json
    {
      "active_region": "AR3684",
      "magnetic_complexity": "BETA-GAMMA-DELTA",
      "similarity_score": 0.88,
      "evolution_stage": "Impulsive Peak",
      "synced_instruments": ["HMI", "AIA", "SoLEXS"]
    }
    ```
*   **Dependencies:** `aditya_flare.multi_modal.digital_twin.solar_state`
*   **Latency:** ~4 ms
*   **Status:** ✅ Fully Implemented
