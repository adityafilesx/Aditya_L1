# Frontend Requirements & Interface Contract — Aditya-L1 Space Weather Platform

This document defines the interface specifications, layout blueprints, chart requirements, UI cards, tables, interaction behaviors, and JSON data structures required to build the modern HTML/CSS/JavaScript frontend dashboard for the Aditya-L1 Space Weather Intelligence Platform.

---

## 1. Page Layouts & Workflows

The frontend consists of a tabbed navigation interface tailored for space weather operators, organized around the **Monitor → Investigate → Respond → Review** lifecycle.

```
+-------------------------------------------------------------------------------------------------+
|  [Logo] Aditya-L1 Mission Control               [Status: WATCH]  [Sim Mode: LIVE]  [Time: UTC]  |
+-------------------------------------------------------------------------------------------------+
|  (Tabs)  [1. Mission Overview]  [2. Operations Center]  [3. Telemetry & Health]                 |
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|  [                                       Main Page View                                      ]  |
|                                                                                                 |
+-------------------------------------------------------------------------------------------------+
```

### Page 1: Mission Overview (Monitor)
*   **Purpose:** Executive/director summary of current solar activity and spacecraft state.
*   **Key Contents:**
    *   Top status strip (Active alerts, current state).
    *   Twin views of the Sun: Solar active region summary map and SDO/AIA imagery placeholders.
    *   3-hour lookahead forecast summary card.
    *   Current payload acquisition mode (Nominal vs. Burst).

### Page 2: Operations Center (Investigate & Respond)
*   **Purpose:** Active operator console for analyzing solar events, triggering overrides, and running simulations.
*   **Layout:** Responsive 12-column grid.
    *   **Columns 1-8:** Flight Recorder timeline controls, synchronized multi-sensor time-series plots, wavelet scalogram, and PSD charts.
    *   **Columns 9-12:** Event Context Panel, Event Inspector, Alert dispatcher, and Operator Notebook (Log of annotations/bookmarks).

### Page 3: Telemetry & Health (Review)
*   **Purpose:** Systems engineering viewport to monitor instrument calibration curves, packet drop statistics, sensor drift values, and model calibration bands.
*   **Key Contents:**
    *   Time-series graphs of telemetry health (SoLEXS vs. HEL1OS packet loss rates).
    *   Drift metric tables showing Kolmogorov-Smirnov (KS) test statistics for features.
    *   Conformal prediction interval overlays mapping actual X-ray flux vs. model uncertainty bounds.

---

## 2. API Data Contract (JSON Schemas)

The frontend communicates with the backend via local/REST JSON APIs. Below are the payload and response schemas.

### API 2.1: Aligned Telemetry & Nowcast Stream
*   **Endpoint:** `/api/telemetry/stream`
*   **Method:** `GET`
*   **Query Parameters:**
    *   `cadence_minutes`: integer (default `1`)
    *   `window_hours`: integer (default `6`)
*   **Response JSON Schema:**
    ```json
    {
      "query_time": "2026-06-25T18:00:00Z",
      "window_start": "2026-06-25T12:00:00Z",
      "window_end": "2026-06-25T18:00:00Z",
      "cadence_minutes": 1,
      "data": [
        {
          "timestamp": "2026-06-25T17:59:00Z",
          "solexs_flux": 1.25e-5,
          "goes_flux_xr": 1.18e-5,
          "hel1os_counts": 420.5,
          "flare_probability": 0.208,
          "uncertainty_lower": 0.18,
          "uncertainty_upper": 0.23,
          "state": "WATCH"
        }
      ]
    }
    ```

### API 2.2: Physics Diagnostics Detail
*   **Endpoint:** `/api/physics/diagnostics`
*   **Method:** `POST`
*   **Request Body JSON:**
    ```json
    {
      "timestamp": "2026-06-25T17:59:00Z",
      "window_minutes": 60
    }
    ```
*   **Response JSON Schema:**
    ```json
    {
      "timestamp": "2026-06-25T17:59:00Z",
      "neupert_derivative": 1.28e-6,
      "psd_peak_power": 48.2,
      "psd_peak_frequency": 0.0033,
      "wavelet_burst_detected": false,
      "entropy_complexity": 0.42,
      "heating_rate": 0.12,
      "cooling_rate": -0.05
    }
    ```

### API 2.3: Operational Recommendation & Alert Status
*   **Endpoint:** `/api/decision/status`
*   **Method:** `GET`
*   **Response JSON Schema:**
    ```json
    {
      "timestamp": "2026-06-25T18:00:00Z",
      "current_state": "WATCH",
      "previous_state": "NOMINAL",
      "alert_level": "PRE_ALERT",
      "recommendation": {
        "action": "Prepare Spacecraft Burst Mode",
        "urgency": "HIGH",
        "scientific_rationale": "Ensemble probability exceeds 20.8% threshold. Neupert derivative shows rapid pre-flare thermal heating (+1.28e-5 W/m²/s). Telemetry quality is nominal.",
        "required_action": "Enable high-cadence payload acquisition loop"
      },
      "active_alarms": [
        {
          "id": "ALARM_098",
          "severity": "WARNING",
          "message": "Neupert thermal pre-heating rate limit exceeded",
          "timestamp": "2026-06-25T17:58:00Z"
        }
      ]
    }
    ```

### API 2.4: Active Region & Knowledge Graph Node Info
*   **Endpoint:** `/api/digital-twin/region`
*   **Method:** `GET`
*   **Query Parameters:**
    *   `region_id`: string (e.g. `AR3684`)
*   **Response JSON Schema:**
    ```json
    {
      "region_id": "AR3684",
      "magnetic_complexity": "BETA-GAMMA-DELTA",
      "similarity_score": 0.88,
      "evolution_stage": "Impulsive Peak",
      "last_observed_coordinates": "N18W42",
      "associated_events": [
        {
          "event_id": "FLARE_20260625_A",
          "type": "C-class Flare",
          "confidence": 0.94,
          "timestamp": "2026-06-25T15:24:00Z"
        }
      ],
      "graph_links": [
        {
          "source": "AR3684",
          "target": "FLARE_20260625_A",
          "relation": "PRODUCED"
        }
      ]
    }
    ```

---

## 3. UI Reusable Component Library

The frontend uses a clean, light-theme aesthetic inspired by Linear.app, Stripe, and Apple dashboards.

### 3.1 UI Cards (Status & Summary Blocks)
1.  **Current Solar Flare Probability Card:**
    *   **Elements:** Large percentage text (e.g. `20.8%`), small sparkline, uncertainty range (`[18.0% - 23.0%]`), and indicator badge (e.g. `🟡 Elevated`).
2.  **Spacecraft Operational State Card:**
    *   **Elements:** Status term (`WATCH` / `ALERT`), indicator light color-mapped to level, duration timer since last transition, and trigger rule descriptor (`Prob > 0.2`).
3.  **Telemetry Ingestion Health Card:**
    *   **Elements:** Overall quality index (`98%`), packets received counts vs. expected, warning tags if packet drop threshold is exceeded, and live ingest heartbeat indicator.
4.  **Action Directive Card (Next Command):**
    *   **Elements:** High-contrast box with a bold command prompt (`ACTION: Enable High-Cadence Burst Mode`), confidence tier (`HIGH`), and plain-language justification block.

### 3.2 UI Tables (Structured Lists)
1.  **Active Regions Table:**
    *   **Columns:** Region ID | Magnetic Class | Spot Area | Growth Trend | Similarity index.
    *   **Interactions:** Row selection updates the active region graph in the Digital Twin view.
2.  **Historical Alert Log Table:**
    *   **Columns:** Timestamp | Severity (Warning/Critical) | Message | Active State | Ack Button.
3.  **Feature Drift Table:**
    *   **Columns:** Feature Name | Baseline Mean | Window Mean | KS-Statistic | Status Alert (Green/Red).

### 3.3 Visualizations & Charts
1.  **X-Ray Flux & Flare Probability Synchronized Timeline (Primary Chart):**
    *   **Type:** Dual-axis line chart (Flux on Left Y, Probability on Right Y).
    *   **Features:** Shared timeline. Moving cursor vertically shows coordinates across both series.
2.  **Wavelet Spectrogram / Scalogram:**
    *   **Type:** Heatmap (Time vs. Scale/Frequency vs. Power).
    *   **Features:** Color gradient mapping spectral density peak areas.
3.  **SHAP Explainability Waterfall Chart:**
    *   **Type:** Horizontal bar chart.
    *   **Features:** Green positive bars (feature increases probability), red negative bars (feature decreases probability) relative to model base value.

---

## 4. Key Interactive Workflows

### 4.1 Switch Mode (Live vs. Demo Simulation)
*   **Control:** Top-right header toggle switches between `LIVE` data ingestion and `DEMO` replay mode.
*   **Behavior:**
    *   `LIVE` mode pulls telemetry via `/api/telemetry/stream` every 60 seconds.
    *   `DEMO` mode pauses real-time reads and enables the Flight Recorder panel.

### 4.2 Shared Event Context & Cursor Sync
*   **Behavior:** When an operator hovers over a data point on the timeline, or selects a historical event in the Alert Log, the timeline cursor moves globally on all charts (X-ray, Wavelet, PSD, and Conformal prediction intervals) to sync analysis.

### 4.3 Operator Flight Recorder Controls
*   **Controls:** Play/Pause, Step-Forward (1 min), Step-Backward (1 min), Jump to Peak, and Speed Multiplier (1x, 5x, 10x, 60x).
*   **Behavior:** Step-by-step playback increments the timestamp context, recalculates the physics features, runs ML inference, and refreshes all UI elements.

### 4.4 Operator Notebook Annotations
*   **Controls:** Text input area, "Bookmark Current Timestamp" button, Category dropdown (Observation, Calibration Alert, Command Action).
*   **Behavior:** Appends record with UTC timestamp to local browser storage, drawing a vertical annotation line on the main synchronized timeline.
