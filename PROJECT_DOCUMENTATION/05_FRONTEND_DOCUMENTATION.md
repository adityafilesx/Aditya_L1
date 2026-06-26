# 05. Frontend Documentation

This document describes the architectural layout, React component trees, stores, and API clients powering the user interface.

---

## 🎛 Global State Architecture

The frontend uses **Zustand** stores for lightweight, high-performance state synchronization across pages:
1.  **`useStreamStore`**: Manages the WS connection to `/ws/live` and caches the latest packets (`TELEMETRY`, `PHYSICS`, `FORECAST`, `MISSION_STATE`, `SYSTEM`, `ALERTS`).
2.  **`useWorkspaceStore`**: Tracks active selections (e.g. active regions, active nodes in the Knowledge Graph, selected times for replay).

---

## 🖥 Page Details & Components

### 1. Mission Overview (`/overview`)
*   **Purpose**: The central dashboard summarizing active mission status, spacecraft health, current GOES flux, and the immediate AI flare forecast.
*   **Key Components**:
    *   `KpiCard`: Displays active metrics (e.g. current GOES class, forecast probability, active regions).
    *   `PlotlyContainer`: Renders real-time timeseries of GOES XRS-B and SoLEXS counts.
*   **Zustand Connection**: Consumes `useStreamStore` for telemetry and forecast updates.
*   **API Calls**: `GET /api/forecast/current`.

### 2. Operations Center (`/operations`)
*   **Purpose**: Real-time telemetry monitoring and command panel.
*   **Key Components**:
    *   `TelemetryStrip`: Grid of live-updating count rates.
    *   `CommandConsole`: Text console letting operators manually override threshold modes or trigger simulated events.
    *   `ReplayController`: Timeline scrubbers to rewind telemetry back to a historical event.
*   **API Calls**: `GET /api/operations/telemetry`, `POST /api/operations/control`.

### 3. Physics Lab (`/investigation/physics`)
*   **Purpose**: Scientific interface for interactive solar physics analysis.
*   **Key Components**:
    *   `WaveletSpectrogram`: Color-mapped Plotly surface showing CWT frequency over time.
    *   `DEMSpectrum`: Power spectral density fits showing temperature (MK) vs emission measure.
*   **Expected Behavior**: Updates in real time every 5 seconds when a new `PHYSICS` package is received over the WebSocket.

### 4. Solar Digital Twin (`/digital-twin`)
*   **Purpose**: Interactive 3D visualization of the Sun, active region hotspots, and sensor view fields.
*   **Key Components**:
    *   `TwinCanvas`: React Three Fiber container configured with lighting, cameras, and controls.
    *   `SolarSphere`: Procedural shader-mapped sphere representing the solar surface.
    *   `ActiveRegions3D`: Dynamically renders 3D rings or mesh markers at active coordinate positions received from the backend state.
*   **Interactions**: Clicking an active region selects it in `useWorkspaceStore`, which automatically updates the side information inspector.

### 5. Knowledge Graph (`/knowledge/graph`)
*   **Purpose**: Interactive node-link network illustrating relationships between active regions, flares, sensors, and research publications.
*   **Key Components**:
    *   `KnowledgeGraphWorkspace`: Renders nodes using `@xyflow/react` (React Flow).
    *   `ScientificInspector`: Displays details on selected node, pulling linked bibliography data.
*   **Sync Logic**: Selecting a region in the Digital Twin automatically focuses on that region node in the Knowledge Graph.

### 6. AI Scientist Workspace (`/research`)
*   **Purpose**: Chat-based AI assistant and research paper drafting workbench.
*   **Key Components**:
    *   `ResearchConversation`: Chat dialogue box with streaming markdown support.
    *   `ExperimentManager`: Panel to execute and track synthetic prediction runs.
    *   `PublicationBuilder`: Formulates LaTeX-formatted reports ready for exportation.
*   **API Calls**: `POST /api/reasoning/analyze` (streams response tokens).
