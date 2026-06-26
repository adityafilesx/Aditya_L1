# 10. API Reference

This document maps out the available REST and WebSocket endpoints exposed by the API Gateway.

---

## 📡 Base Endpoint Config
*   **Production Host**: `http://localhost:8000`
*   **WebSocket Protocol**: `ws://localhost:8000/ws/live`

---

## 🔗 REST Endpoints

### 1. GET `/api/system/health`
*   **Purpose**: Checks API server responsiveness.
*   **Response**:
    ```json
    {
      "status": "healthy",
      "timestamp": "2026-06-26T02:00:00Z"
    }
    ```
*   **Average Latency**: <5 ms.

### 2. GET `/api/system/diagnostics`
*   **Purpose**: Returns the internal health and process matrices of all sub-engines.
*   **Response**:
    ```json
    {
      "cpu_usage_pct": 14,
      "ram_usage_pct": 42,
      "websocket_clients": 1,
      "background_generator_status": "ONLINE",
      "ai_engine_status": "ONLINE",
      "physics_engine_status": "ONLINE"
    }
    ```

### 3. GET `/api/operations/telemetry`
*   **Purpose**: Retrieves the latest active telemetry packet.
*   **Response**:
    ```json
    {
      "timestamp": "2026-06-26T02:00:00.000Z",
      "goes_xrs_b": 1.2e-7,
      "solexs_sdd2_ctr": 25.4,
      "helios_czt_broad_ctr": 12.1,
      "proton_flux_10MeV": 0.05
    }
    ```

### 4. GET `/api/physics/summary`
*   **Purpose**: Returns physical parameters (temperature, DEM, etc.).
*   **Response**:
    ```json
    {
      "temperature_mk": 12.4,
      "neupert_score": 0.65,
      "emission_measure_norm": 1.2e48,
      "spectral_centroid": 0.52
    }
    ```

### 5. GET `/api/forecast/current`
*   **Purpose**: Returns the current 1-hour forecast and GOES calibration details.
*   **Response**:
    ```json
    {
      "probability": 0.12,
      "confidence": 0.85,
      "estimated_goes_class": "Quiet"
    }
    ```

### 6. GET `/api/forecast/horizons`
*   **Purpose**: Retrieves predictions across multiple temporal windows.
*   **Response**:
    ```json
    {
      "15m": { "probability": 0.1, "confidence": 0.84, "estimated_goes_class": "Quiet" },
      "6h": { "probability": 0.0, "confidence": 0.5, "estimated_goes_class": "Quiet" }
    }
    ```

### 7. GET `/api/digital-twin/state`
*   **Purpose**: Retrieves active region clusters and coordinate mappings.
*   **Response**:
    ```json
    {
      "global_state": "NOMINAL",
      "similarity_score": 0.94,
      "active_regions": {}
    }
    ```

### 8. GET `/api/knowledge-graph/`
*   **Purpose**: Returns graph configuration schemas and details.
*   **Response**:
    ```json
    {
      "num_nodes": 45,
      "num_edges": 120
    }
    ```

### 9. POST `/api/reasoning/analyze`
*   **Purpose**: Executes AI Scientist query processing and context synthesis.
*   **Request Payload**:
    ```json
    {
      "query": "Explain today's flare"
    }
    ```
*   **Response**:
    ```json
    {
      "content": "### 🔴 Mission Status: HIGH ALERT\n\nThe solar low-energy sensors indicate...",
      "confidence": 0.95,
      "sources": [
        { "title": "Mission Intelligence Engine", "module": "mission_intelligence" }
      ]
    }
    ```

---

## 🔌 WebSocket Gateway `/ws/live`
*   **Method**: `WS`
*   **Purpose**: Real-time packet distribution.
*   **Output Payload Format**:
    ```json
    {
      "type": "TELEMETRY",
      "payload": {
        "timestamp": "2026-06-26T02:00:00Z",
        "goes_xrs_b": 1.2e-7,
        "solexs_sdd2_ctr": 25.4
      }
    }
    ```
*   *Emitted types*: `TELEMETRY`, `PHYSICS`, `FORECAST`, `MISSION_STATE`, `SYSTEM`, `ALERTS`, `DIGITAL_TWIN`.
