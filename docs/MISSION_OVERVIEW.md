# Aditya-L1 Mission Overview Architecture

## Overview

The Mission Overview page is the primary dashboard for the Aditya-L1 platform, designed for immediate situational awareness within 5 seconds of loading. It aggregates AI, Physics, Telemetry, and System Health data into a single, cohesive view.

## Architectural Changes (Milestone 2)

We transitioned from a monolithic file approach to a modular package structure to ensure maintainability and scalability.

### Service Layer (`ui/services`)

The UI components no longer generate synthetic data directly or communicate with the backend. Instead, they call functions from the `ui/services` layer.

- **`mission_service.py`**: Provides overall mission state, risk levels, and the dynamic text briefing.
- **`physics_service.py`**: Supplies thermodynamic variables, Neupert scores, and phase space data.
- **`forecast_service.py`**: Aggregates AI model predictions and consensus scores.
- **`sensor_service.py`**: Tracks payload availability, quality, and latency.
- **`system_service.py`**: Monitors backend engine health.
- **`alert_service.py`**: Fetches the latest mission-critical notifications.
- **`digital_twin_service.py`**: Supplies telemetry for the 3D active region viewer.
- **`knowledge_graph_service.py`**: Provides contextual relationships between events.
- **`ai_service.py`**: Monitors the fusion engine and AI pipeline health.

### Modular Package (`ui/pages/mission_overview`)

The page is assembled in `page.py`, which invokes individual section components:

1. **`status_strip.py`**: A horizontal ticker displaying live subsystem statuses.
2. **`quick_actions.py`**: Top-right toolbar for common actions (Refresh, Fullscreen, Logs).
3. **`briefing.py`**: The most critical widget; a plain-text synthesis of the current mission state.
4. **`banner.py`**: High-level status badges (Mission Mode, UTC, AI Status).
5. **`metrics.py`**: Grouped KPI cards (Mission, Physics, System).
6. **`telemetry.py`**: Live Plotly charts for SoLEXS/HEL1OS flux and Forecast probability.
7. **`ai_consensus.py`**: Detailed breakdown of the ensemble models and their agreement.
8. **`physics.py`**: Expanded thermodynamic summary and phase-space hysteresis loop.
9. **`sensor_health.py`**: Data table mapping payload latency and quality.
10. **`digital_twin.py`**: Preview card for the interactive 3D viewer.
11. **`knowledge_graph.py`**: Preview card for relational intelligence mapping.
12. **`timeline.py`**: Unified narrative sequence of recent events.
13. **`system_health.py`**: Status matrix for backend infrastructure.
14. **`alerts.py`**: Filterable list of recent anomaly warnings.

## Data Flow

```
UI Components (Mission Overview Package)
        │
        ▼
Service Layer (ui/services)
        │
        ▼
Backend Engines (aditya_flare)
```

This strict separation of concerns allows for the backend models (e.g., XGBoost, TCN) to be hot-swapped without modifying the frontend view components.
