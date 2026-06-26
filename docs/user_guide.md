# User Guide

## Running the Dashboard

To launch the real-time space-weather dashboard:

```bash
streamlit run aditya_flare/visualization/dashboard.py
```

## Running Model Training

To retrain the XGBoost model, generate explainability (SHAP) plots, and run benchmarks:

```bash
python scripts/train_xgboost.py
```

Check the `data/evaluation/` directory for generated scientific reports, SHAP plots, and reliability diagrams.

## Configuration

Edit `aditya_flare/config/settings.yaml` to modify calibration constants, logging levels, and flare thresholds without altering the source code.
