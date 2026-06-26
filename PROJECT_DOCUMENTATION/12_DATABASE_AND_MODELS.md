# 12. Database & Models

This document details all model files, weights, configuration definitions, and datasets stored locally.

---

## 🗄️ Database layout & local storage

The platform uses a file-based storage layout inside `backend/data/`:

*   **`raw/`**: Directory containing raw spacecraft files (FITS, CSV downlinks).
*   **`processed/`**: Cleaned parquet files (e.g. `goes/`, `20240212/` directories).
*   **`feature_store/`**: Preprocessed feature vectors used for training.
*   **`models/`**: Holds binary weights and JSON estimators.

---

## 🤖 Model weights & serialized objects

### 1. Ensemble Forecaster (`backend/data/models/ensemble_forecaster.pkl`)
*   **Format**: Python Pickle file.
*   **Size**: ~40.2 MB.
*   **Contents**: Serialized scikit-learn pipeline wrapping:
    *   Scale parameters (mean, variance vectors for inputs).
    *   Meta-classifier logistic regression coefficients.
*   **Loader Code**:
    ```python
    import joblib
    model = joblib.load("backend/data/models/ensemble_forecaster.pkl")
    ```

### 2. Nowcast XGBoost (`backend/data/models/xgboost_nowcast.json`)
*   **Format**: XGBoost JSON Model format.
*   **Size**: ~168 KB.
*   **Contents**: Decision tree splits and leaf weight structures.
*   **Loader Code**:
    ```python
    import xgboost as xgb
    model = xgb.Booster()
    model.load_model("backend/data/models/xgboost_nowcast.json")
    ```

---

## 📄 Key Parquet Datasets

### 1. `goes/` & `solexs/` files
*   **Format**: Apache Parquet.
*   **Contents**: High-frequency 1Hz sensor readings used to reconstruct historical flare profiles during Replay.
*   **Key columns**: `goes_flux`, `solexs_count_rate`, `temperature`, `emission_measure`.

---

## ⚙️ Configuration Files

### 1. Alert Thresholds Configuration (`backend/aditya_flare/config/thresholds.yaml`)
*   **Purpose**: Manages decision boundaries for warning states.
*   **Schema**:
    ```yaml
    watch_threshold: 0.60
    alert_threshold: 0.85
    conformal_confidence_alpha: 0.10  # 90% confidence bands
    ```
*   *Implementation could not be determined for dynamic remote database sync, but local file fallback works.*
