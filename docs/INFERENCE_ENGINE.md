# Inference Engine

In accordance with architectural separation, real-time forecast inference is deferred to **Milestone 6**.

## Planned Flow in Milestone 6

```
Load Active Model
       ↓
Load Feature Vector (Feature Store)
       ↓
Run Inference (Forward Pass)
       ↓
Calibrate Probability (Calibration Engine)
       ↓
Generate ScientificPrediction Object
       ↓
Publish Output to Mission Dashboard & Uplink
```
