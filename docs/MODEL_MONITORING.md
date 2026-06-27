# Model Monitoring

Model Monitoring tracks data distributions, prediction stability, and operational metrics.

## Drift Calculations

- **Population Stability Index (PSI)**: Quantifies change in distribution between reference dataset (training) and incoming target data (online inference stream).
  - $PSI < 0.1$: No significant change (Nominal).
  - $0.1 \le PSI < 0.25$: Moderate drift (Warning).
  - $PSI \ge 0.25$: Severe drift (Degraded, trigger retrain).
- **Data Drift**: Shifts in raw telemetry inputs.
- **Feature Drift**: Shifts in engineered features.
- **Prediction Drift**: Changes in predicted output class frequencies.
- **Calibration Drift**: Increases in ECE over time.
