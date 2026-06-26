# Aditya-L1 Mission Control Visualization Engine

## Overview
The frontend Visualization Engine is designed to support real-time rendering of scientific and operational telemetry. Built on React 18, it leverages Plotly.js, Three.js, React Three Fiber, D3, and React Flow to offer rich, responsive, and synchronized dashboards.

## Core Dependencies
*   **Plotly.js (`react-plotly.js`)**: Real-time timeseries, XSPEC plots, phase-space rendering, CWT scalograms.
*   **Three.js / React Three Fiber**: The Digital Twin system, enabling interactive 3D visualizations of the solar surface and magnetic fields at high FPS.
*   **D3 / React Flow**: Network and Knowledge Graph rendering (pipeline traceability).
*   **Zustand**: Cross-component synchronization. Two separate stores are utilized:
    *   `streamStore`: Stores high-frequency telemetry, predictions, and physics data. Includes a rolling history buffer for Plotly ingestion.
    *   `workspaceStore`: Manages the interactive state across the UI (synchronized cursors, time scrubbing, and playback).

## Global Timeline & Synchronization
To provide a cohesive "scientific workstation" feel, all Plotly charts support a `syncCursor` property. When a user hovers or scrubs the global `MissionTimeline` (or any synchronized Plotly instance), `workspaceStore.setCursorTime` is triggered. All subscribed plots will instantly draw a cursor line at that exact UTC time.

## Workspaces Supported
1.  **OperationsPage (Telemetry)**: Plotly timeseries for Multi-wavelength Soft X-ray and Proton Fluxes.
2.  **PhysicsLabPage (Physics)**: Temperature-Emission phase space analysis, Neupert scoring, and continuous energy spectra rendering.
3.  **ResearchPage (Spectral & Wavelet)**: High-resolution Plotly heatmaps representing Continuous Wavelet Transforms (CWT) and synthetic canvas image viewers.
4.  **DigitalTwinPage (3D/2D Viewer)**: WebGL-based Three.js rendering of the sun's surface overlaid with real-time AR tagging and anomaly detection.
5.  **AiWorkspacePage (Explainability)**: Real-time Plotly charts modeling live probability confidence intervals alongside SHAP explainability matrices.

## Export Engine Capabilities
Data from any `PlotlyContainer` can be immediately exported. Plotly's ModeBar allows direct extraction to PNG/SVG, while raw array states can be parsed into CSV for downstream analytics (i.e. Jupyter notebook integrations).

## Performance Guidelines
*   **History Buffers**: The telemetry stream slices arrays dynamically. Do not allow `history.telemetry.length` to exceed 1000 items in the browser to prevent Canvas/SVG memory bloat.
*   **WebGL**: Always wrap Three.js contexts in `<WebGLErrorBoundary>` and clean up unmounted geometries/materials recursively. Use `IntersectionObserver` to pause rendering when the canvas is hidden.
*   **Suspense & Code Splitting**: Charts are heavy. Utilize `React.lazy()` for all route components containing complex Plotly or WebGL renders.
