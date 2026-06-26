# Aditya-L1 Mission API Contracts (Phase FE-5 Draft)

## Overview
This document outlines the standard contracts to be implemented between the Frontend (`/src/services/`) and Backend (`FastAPI`) during the next integration phase.

## 1. REST APIs (HTTP)

### 1.1 Digital Twin Physics State
`GET /api/v1/physics/state`
Returns the current physics state including magnetic fields, thermodynamics, and energy calculations.

**Response Schema (Example):**
```json
{
  "magnetic_energy": 4.5e28,
  "neupert_correlation": 0.82,
  "thermal_energy": 1.2e30,
  "timestamp": "2024-02-12T14:30:00Z"
}
```

### 1.2 Space Weather Forecast
`GET /api/v1/forecast/nowcast`
Returns the latest ML model prediction for solar flare likelihood.

**Response Schema:**
```json
{
  "probability_M_class": 0.85,
  "probability_X_class": 0.12,
  "flare_expected_window": "2-4h",
  "confidence": 0.94
}
```

## 2. WebSockets

### 2.1 Live Telemetry Stream
`WS /ws/telemetry`
Streams live HEL1OS, SUIT, and SoLEXS instrument data.

**Message Event Schema:**
```json
{
  "type": "telemetry_update",
  "instrument": "HEL1OS",
  "data": {
    "flux_10_30keV": 142.5,
    "flux_30_100keV": 45.2
  },
  "timestamp": "2024-02-12T14:30:01Z"
}
```
