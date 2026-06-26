# 13. User Manual

This manual explains how to interact with the Aditya-L1 Space Weather Intelligence Platform to monitor, analyze, and predict solar flares.

---

## 🧭 Dashboard Sections

The sidebar menu groups capabilities into five main screens:

```
[Overview] ---> [Operations] ---> [Physics Lab] ---> [Digital Twin] ---> [Knowledge Graph] ---> [AI Scientist]
```

---

## 📈 1. Mission Overview Screen
When you first log in, you are presented with the **Mission Overview**.
*   **Mission Banner**: Located at the top, showing the current system state (`NOMINAL`, `WATCH`, `ALERT`).
*   **KPI Metrics**: Displays current GOES flux value, 1-hour forecast probability, and number of active region groups visible on the Sun.
*   **Active Plots**: Observe the live timeseries chart showing incoming counts from the SoLEXS sensor.

---

## 🚨 2. Operations Center
Used by payload operators to configure warning states and review historical events:
*   **Replay Scrubber**: Click a point on the historical timeline to scrub back. The dashboard will enter **Replay Mode**, reloading telemetry from that period. Click "Resume Live" to return to real-time telemetry.
*   **Alert Panel**: Displays a table of all system and physical threshold warnings.
*   **Command Console**: Input shell commands to manually force instrument warning levels or trigger calibration cycles.

---

## 🌡️ 3. Physics Lab
Designed for solar physicists analyzing raw emission shapes:
*   **Spectrogram Analysis**: Hover over the wavelet spectrogram chart to view power levels at specific periods.
*   **Differential Emission Measure**: Inspect the DEM plot to see the electron temperature fit.

---

## 🌞 4. Solar Digital Twin
Provides an interactive 3D rendering of the Sun:
*   **Orbit Controls**: Click and drag your mouse to rotate the Sun. Scroll to zoom.
*   **Active Regions**: Yellow markers represent active regions (e.g. AR 13664). Hovering over a marker shows its heliographic coordinates.
*   **Layers Selector**: Toggle between **Photosphere** (visible surface), **Magnetogram** (magnetic field polarities), and **Corona** (high-temperature outer atmosphere).

---

## 🕸️ 5. Knowledge Graph
Explores relationship pathways between solar structures:
*   **Canvas Layout**: Drag nodes representing active regions, flares, or spacecraft. Double-click a node to fetch and draw its connections.
*   **Search Bar**: Search for historical flares (e.g., "X8.7 Flare") to map their nodes onto the workspace.

---

## 🤖 6. AI Scientist
Interact with the Scientific Reasoning Engine:
1.  Navigate to `/research`.
2.  Input a question in the chat bar (e.g., "How does today's soft X-ray curve compare with the Carrington Event?").
3.  Press Enter. The assistant will display a structured markdown response with citations.
