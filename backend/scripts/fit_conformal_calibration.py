import os
import sys
import yaml
import numpy as np
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from aditya_flare.models.dataset import load_and_prepare_dataset, get_train_test_split
from aditya_flare.config.config_loader import config
from aditya_flare.utils.logger import training_logger
import xgboost as xgb

def fit_conformal():
    processed_dir = Path(config.processed_dir)
    models_dir = Path(config.models_dir)
    calib_dir = Path("aditya_flare/calibration")
    calib_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Load dataset (using same logic as train_xgboost)
    training_logger.info("Loading dataset for Conformal Calibration...")
    try:
        df = load_and_prepare_dataset(processed_dir, target_threshold=config.target_threshold_cps, horizon_minutes=config.horizon_minutes)
    except Exception as e:
        training_logger.error(f"Error loading dataset: {e}")
        return

    # Use the chronological test set as the calibration set
    X_train, X_test, y_train, y_test = get_train_test_split(df, test_size=0.2)
    
    # 2. Load model
    model_path = models_dir / "xgboost_nowcast.json"
    if not model_path.exists():
        training_logger.error(f"XGBoost model not found at {model_path}!")
        return
        
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    
    # 3. Get predictions on the calibration (test) set
    training_logger.info("Running inference on calibration set...")
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # 4. Calculate Nonconformity scores
    # For binary classification mapped to probability, a simple nonconformity score is 
    # the absolute error between true label (0 or 1) and predicted probability.
    scores = np.abs(y_test - y_pred_proba)
    
    # 5. Calculate conformal threshold Q_1-alpha
    alpha = 0.10 # 90% confidence
    n = len(scores)
    
    q = np.quantile(scores, 1 - alpha)
    
    training_logger.info(f"Conformal Calibration completed on {n} samples.")
    training_logger.info(f"Computed Q_90% nonconformity threshold: {q:.4f}")
    
    # 6. Save to config
    config_path = calib_dir / "conformal_config.yaml"
    out_data = {
        "alpha": alpha,
        "n_calibration_samples": n,
        "q_threshold": float(q),
        "method": "absolute_residual"
    }
    
    with open(config_path, "w") as f:
        yaml.dump(out_data, f)
        
    training_logger.info(f"Saved Conformal bounds to {config_path}")

if __name__ == "__main__":
    fit_conformal()
