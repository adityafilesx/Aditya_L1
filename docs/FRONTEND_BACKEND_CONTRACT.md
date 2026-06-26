# Frontend-Backend API Contract Specification — Aditya-L1 Platform

This document describes the JSON payloads, request schemas, REST API responses, and WebSocket streams for communication between the frontend client and the web service.

---

## 1. REST API Contracts

### 1.1 Ingest Stream Overview
*   **Path:** `/api/v1/telemetry/stream`
*   **Method:** `GET`
*   **Query Parameters:**
    *   `window_hours` (integer, default `6`): Time-series window size.
    *   `cadence_minutes` (integer, default `1`): Sampling step interval.
*   **Response Payload (JSON):**
    ```json
    {
      "status": "success",
      "timestamp": "2026-06-25T18:00:00Z",
      "window_start": "2026-06-25T12:00:00Z",
      "window_end": "2026-06-25T18:00:00Z",
      "data": [
        {
          "time": "2026-06-25T17:59:00Z",
          "solexs_flux": 1.25e-5,
          "hel1os_flux": 3.42e-7,
          "goes_flux": 1.18e-5,
          "flare_prob": 0.208,
          "state": "WATCH"
        }
      ]
    }
    ```

### 1.2 Physics Diagnostics
*   **Path:** `/api/v1/physics/diagnostics`
*   **Method:** `POST`
*   **Headers:** `Content-Type: application/json`
*   **Request Body (JSON):**
    ```json
    {
      "timestamp": "2026-06-25T18:00:00Z",
      "channel": "solexs_sdd2"
    }
    ```
*   **Response Payload (JSON):**
    ```json
    {
      "timestamp": "2026-06-25T18:00:00Z",
      "diagnostics": {
        "neupert_score": 0.82,
        "spectral_entropy": 0.38,
        "spectral_flatness": 0.05,
        "temperature_mk": 14.2,
        "emission_measure": 1.2e48,
        "wavelet_anomaly": false
      }
    }
    ```

### 1.3 AI Explainability (SHAP Values)
*   **Path:** `/api/v1/explainability/shap`
*   **Method:** `GET`
*   **Query Parameters:**
    *   `timestamp` (string, required): Prediction timestamp.
*   **Response Payload (JSON):**
    ```json
    {
      "timestamp": "2026-06-25T18:00:00Z",
      "base_value": 0.15,
      "prediction_value": 0.208,
      "features": [
        {
          "name": "solexs_flux_derivative",
          "value": 1.28e-5,
          "shap_value": 0.042
        },
        {
          "name": "hel1os_counts",
          "value": 420.5,
          "shap_value": 0.016
        }
      ]
    }
    ```

---

## 2. WebSocket Real-Time Interface

To support real-time data streaming without polling overhead, the frontend opens a WebSocket connection to the backend.

*   **URL:** `ws://<backend_host>/api/v1/telemetry/live`
*   **Events Streamed (Server to Client):**

### 2.1 Telemetry Heartbeat Event
Exposes live sensor readings as they arrive:
```json
{
  "event": "telemetry_update",
  "data": {
    "timestamp": "2026-06-25T18:01:00Z",
    "solexs_sdd2_ctr": 1540.2,
    "hel1os_counts": 421.0,
    "goes_flux": 1.19e-5
  }
}
```

### 2.2 Alert Trigger Event
Dispatched when the state machine transitions or an alarm threshold is crossed:
```json
{
  "event": "alert_triggered",
  "data": {
    "alert_id": "ALERT_20260625_A",
    "timestamp": "2026-06-25T18:01:00Z",
    "previous_state": "WATCH",
    "current_state": "ALERT",
    "severity": "CRITICAL",
    "message": "Model flare probability exceeds 20.8% threshold. Triggering payload high-cadence burst acquisition mode.",
    "recommendation": "Transition spacecraft to ALERT mode immediately."
  }
}
```

### 2.3 Drift Warning Event
Dispatched when sensor drift exceeds baseline thresholds:
```json
{
  "event": "drift_warning",
  "data": {
    "timestamp": "2026-06-25T18:00:00Z",
    "feature_name": "solexs_sdd2_ctr",
    "ks_statistic": 0.082,
    "p_value": 0.004,
    "message": "Kolmogorov-Smirnov test flags substantial input telemetry distribution drift. Calibrations may need updating."
  }
}
```
