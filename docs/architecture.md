# Architecture Guide

The Aditya-L1 Solar Flare Forecasting System utilizes a dual-segment architecture:

## 1. Ground Segment (Machine Learning)
- Python-based pipeline using `XGBoost`.
- Integrates `SHAP` for explainable AI.
- `aditya_flare.evaluation` provides scientific metrics (TSS, HSS, Brier, ECE, MCE).
- `aditya_flare.calibration` converts instrument counts to physical GOES W/m² flux values.

## 2. Space Segment (Deterministic State Machine)
- Sub-millisecond latency C-compatible Python module (`aditya_flare.models.space_trigger`).
- Implements purely deterministic states without ML dependencies.
- Avoids floating-point heavy operations where possible.

## 3. Configuration & Logging
- YAML-based centralized configuration (`config/settings.yaml`).
- Standardized rotating logs for inference, training, and dashboard components.
