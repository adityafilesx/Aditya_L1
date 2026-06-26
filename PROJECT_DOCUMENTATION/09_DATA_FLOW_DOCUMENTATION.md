# 09. Data Flow Documentation

This document describes how telemetry packets flow through the systems and transform at each stage.

---

## 🌊 Complete Data Pipeline Path

```
 [ Spacecraft Instruments ] (Downlink)
             |
             v
 [ Raw Ingestion Engine ] (Telemetry packets emitted)
             |
             v
      (Mission Event Bus)
      /       |         \
     /        |          \
    v         v           v
[Physics]  [Nowcast]  [WS Streaming] -------> [Frontend UI]
    |         |
    +----+----+
         |
         v
 [Feature Pipeline] (Preprocessed tensors)
         |
         v
  [Forecast Engine] (Ensemble predictions)
         |
         v
 [Decision Engine] (State machine trigger)
         |
         v
[Mission Intelligence] (System alerts / warnings)
         |
         v
[Knowledge Graph & SRE] (Graph links, RAG Context)
```

---

## 🔬 Processing Stages

### 1. Spacecraft Telemetry Ingestion
Spacecraft downlinks raw X-ray count data. The platform's ingestion workers read these files or streams, producing standard dictionary structures containing:
*   `goes_xrs_a`: Short-band X-ray flux.
*   `goes_xrs_b`: Long-band X-ray flux.
*   `solexs_sdd2_ctr`: Soft X-ray counts.
*   `helios_czt_broad_ctr`: Hard X-ray counts.

### 2. Physics Transform
Raw parameters are evaluated by the Physics Engine to compute physical parameters:
*   **Temperature (MK)**: Reflects flare plasma heating.
*   **Emission Measure**: Indicates plasma quantity.
*   **Neupert score**: Correlates soft X-ray derivatives with hard X-rays.

### 3. Feature Assembly
Calculated physical values and raw sensor values are combined into a standardized vector:
```
[ goes_flux, goes_flux_derivative, temperature, EM, wavelet_power_1, wavelet_power_2 ]
```

### 4. Ensemble Forecast
The feature vector is passed to the TCN, Transformer, and XGBoost models. The outputs are averaged and calibrated via conformal prediction intervals to produce a probability vector over 15m to 6h horizons.

### 5. Decision & Mission State State Machine
The Decision Engine reads the forecast values. If the probability of an X-class flare in the next hour exceeds 80%, it transitions the mission state from `NOMINAL` to `ALERT`, sending the state update over WebSockets.

### 6. Knowledge Graph Linking & SRE Context
The forecast triggers an automatic graph updates inside the Knowledge Graph. If the AI Scientist is queried, it reads the updated graph structure and provides explanations.

### 7. UI Presentation
The Frontend parses the WS packets, instantly updating the Plotly charts, Three.js Digital Twin, React Flow graph, and SRE chat window.
