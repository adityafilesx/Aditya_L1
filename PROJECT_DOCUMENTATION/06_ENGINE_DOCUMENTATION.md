# 06. Engine Documentation

This document explains the algorithms, workflows, and inputs/outputs of the 11 engines running on the platform.

---

## 📡 1. Telemetry Engine
*   **Purpose**: Pulls and standardizes satellite count streams (Goes XRS, SoLEXS).
*   **Inputs**: Spacecraft downlink file streams (e.g. FITS or CSV telemetry indices).
*   **Outputs**: Cleaned JSON telemetry frames emitted at a 1 Hz rate.
*   **Connected Modules**: Mission Event Bus, Nowcasting Engine.

---

## ⚡ 2. Feature Pipeline
*   **Purpose**: Preprocesses raw telemetry frames into structured ML vectors.
*   **Algorithm**: Normalizes counts, calculates log ratios, computes derivatives of flux curves, and stacks historical lag vectors.
*   **Dependencies**: NumPy, Pandas.

---

## 🌡️ 3. Physics Engine
*   **Purpose**: Translates radiative flux into physical thermodynamics parameters.
*   **Outputs**: `electron_temperature_mk`, `emission_measure_norm`, `shannon_entropy`.
*   **Algorithms**:
    *   **Differential Emission Measure (DEM)**: Estimated via ratios of Soft X-ray fluxes.
    *   **Neupert Correlation**: Checks if hard X-ray flux tracks the derivative of soft X-ray flux:
        $$F_{SXR}(t) \propto \int^t F_{HXR}(\tau) d\tau$$
    *   **Shannon Entropy**: Measures intensity profile flatness.

---

## 🔮 4. Forecast Engine
*   **Purpose**: Runs multi-horizon flare prediction pipelines.
*   **Inputs**: Physics-feature vectors.
*   **Algorithms**: Stacks predictions from a TCN, Transformer, and XGBoost classifier. Employs Conformal Prediction to produce exact error bounds.
*   **Outputs**: Probabilities of M or X-class flares occurring in 15m, 30m, 1h, 3h, and 6h horizons.

---

## ⏱️ 5. Nowcasting Engine
*   **Purpose**: Instantaneous event detection (detecting if a flare is currently underway).
*   **Algorithm**: Evaluates a high-speed gradient-boosted decision tree on instantaneous count rates and derivative vectors.
*   **Output**: State: `Quiet` (0), `Rise` (1), `Peak` (2), `Decay` (3).

---

## 🚦 6. Decision Engine
*   **Purpose**: Translates forecast probabilities into payload scheduling alerts.
*   **Algorithm**: Evaluates trigger conditions over forecast matrices.
*   **Outputs**: Mission Status overrides (`NOMINAL`, `WATCH`, `ALERT`).

---

## 🛰️ 7. Mission Intelligence
*   **Purpose**: Generates high-level recommendations and evaluates system risk indexes.
*   **Algorithm**: Fuzzy logic combining forecast probabilities, instrument health status, and sensor noise indexes.

---

## 🌊 8. Streaming Engine
*   **Purpose**: Orchestrates event delivery to the user interface.
*   **Algorithm**: Asynchronous asyncio-based publish-subscribe broker (`MissionBus`).
*   **Connected Modules**: Live WebSocket API endpoint (`/ws/live`).

---

## 🌞 9. Solar Digital Twin
*   **Purpose**: Generates physical surface coordinates and active region configurations.
*   **Inputs**: Carrington heliographic coordinates of sunspot clusters.
*   **Outputs**: 3D mesh translations, rotation vectors, and layer overlay properties.

---

## 🕸️ 10. Knowledge Graph
*   **Purpose**: Manages connections between telemetry anomalies and historical occurrences.
*   **Algorithm**: RDF graph database simulation (in-memory adjacency list).
*   **Outputs**: Node-link matrices representing solar weather states.

---

## 🤖 11. Scientific Reasoning Engine (SRE)
*   **Purpose**: Executes LLM agent plans to analyze data and draft research drafts.
*   **Algorithm**: LangGraph cyclic routing checking context validity.
*   **Connected Modules**: `/api/reasoning/analyze` endpoint.
