# 08. Feature Encyclopedia

This encyclopedia lists and describes every interactive feature available in the Space Weather Intelligence Platform.

---

## 📊 Feature 1: Real-Time Telemetry Plotting
*   **Purpose**: Displays satellite sensors' count rates as they arrive.
*   **Why it exists**: Operators must instantly spot sudden flux jumps indicating the onset of a solar flare.
*   **User Workflow**: Opens `/overview` or `/operations`. The charts automatically update.
*   **Backend Workflow**: Ingestion workers read raw inputs, emit them onto the Event Bus, and the WebSocket stream sends them to clients.
*   **Frontend Workflow**: `useStreamStore` catches the packet and updates the Plotly timeseries buffer.
*   **Connected APIs**: WebSocket `/ws/live`.
*   **Connected Engines**: Telemetry Engine, Streaming Engine.
*   **Expected Output**: Line charts showing GOES X-ray fluxes (0.1–0.8 nm) and SoLEXS count rates.
*   **Failure Cases**: If the WebSocket drops, the chart halts. The UI shows a reconnecting indicator.

---

## 🌡️ Feature 2: Thermodynamic Spectral Fit
*   **Purpose**: Computes flare temperature and emission measure.
*   **Why it exists**: Confirms if the plasma temperature is rising, indicating flare heating.
*   **User Workflow**: Navigates to `/investigation/physics` to view the DEM Spectrum chart.
*   **Backend Workflow**: The Physics Engine reads Soft X-ray fluxes, computes temperature, and publishes results.
*   **Connected APIs**: `GET /api/physics/summary`.
*   **Connected Engines**: Physics Engine.

---

## 🔮 Feature 3: Multi-Horizon Forecasting
*   **Purpose**: Predicts flare probabilities up to 6 hours ahead.
*   **Why it exists**: Gives mission command early warning to prepare payloads or alert power grids.
*   **User Workflow**: View the "Forecasting" card on the Overview dashboard.
*   **Backend Workflow**: Executes ensemble inference on raw count buffers.
*   **Connected APIs**: `GET /api/forecast/horizons`.
*   **Connected Engines**: Forecast Engine.

---

## 🌞 Feature 4: Interactive Solar Digital Twin
*   **Purpose**: 3D representation of the Sun with active regions.
*   **Why it exists**: Provides a spatial context for numerical measurements.
*   **User Workflow**: Navigates to `/digital-twin`. Rotates the 3D sphere, clicks active region nodes, and changes layers (magnetic field, corona).
*   **Backend Workflow**: Synthesizes solar coordinates into active region lists.
*   **Connected APIs**: `GET /api/digital-twin/state`.
*   **Connected Engines**: Digital Twin Engine.

---

## 🕸️ Feature 5: Knowledge Graph Exploration
*   **Purpose**: Visualizes relationships between active regions and publications.
*   **Why it exists**: Helps scientists retrieve historical analogies for the active regions currently visible.
*   **User Workflow**: Navigates to `/knowledge/graph`. Double clicks nodes to expand links, and searches for historical events.
*   **Connected APIs**: `GET /api/knowledge-graph/`.
*   **Connected Engines**: Knowledge Graph Engine.

---

## 🤖 Feature 6: AI Scientist Workspace (SRE)
*   **Purpose**: Assistant that reasons over the system's live state.
*   **Why it exists**: Autonomously drafts reports and answers scientific queries.
*   **User Workflow**: Navigates to `/research`. Types "Explain today's flare" and submits.
*   **Backend Workflow**: Compiles context from `app_state` and queries LLM router.
*   **Connected APIs**: `POST /api/reasoning/analyze`.
*   **Connected Engines**: Scientific Reasoning Engine.
