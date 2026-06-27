import os
import sys
import time
import signal
import logging
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import pickle

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.aditya_flare.config.config_loader import config, reload_config
from backend.aditya_flare.decision.state_machine import DecisionEngine
from backend.aditya_flare.utils.logger import decision_logger, telemetry_logger, inference_logger
from backend.aditya_flare.processing.features import extract_features

logger = logging.getLogger("daemon")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

running = True

def signal_handler(sig, frame):
    global running
    logger.info("Termination signal received. Shutting down daemon gracefully...")
    running = False

def run_daemon():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("Initializing 24/7 Operations Daemon...")
    decision_engine = DecisionEngine()
    
    model_path = Path("data/models/ensemble_forecaster.pkl")
    if not model_path.exists():
        logger.error("Ensemble model not found. Run training first.")
        return
        
    with open(model_path, "rb") as f:
        ensemble_data = pickle.load(f)
        
    logger.info("Entering main telemetry polling loop. Waiting for new data...")
    
    # We simulate a "live" stream by reading the last N minutes from the compiled parquet
    # and shifting our "current_time" forward every cycle.
    processed_dir = Path(config.processed_dir)
    df = extract_features(processed_dir, max_days=1, flare_threshold=100.0)
    if df.empty:
        logger.error("No telemetry found to simulate stream.")
        return
        
    # Start simulating from the middle of the dataframe
    start_idx = len(df) // 2
    
    poll_interval_sec = 2 # Simulate 1 minute of telemetry every 2 seconds
    
    for i in range(start_idx, len(df)):
        if not running:
            break
            
        # Hot-reload config automatically at each cycle
        reload_config()
        
        current_time = df.index[i]
        row = df.iloc[i]
        
        # 1. Simulate Ground ML Inference
        features_dict = row.to_dict()
        X = row[ensemble_data['features']].values.reshape(1, -1)
        p_lgb = ensemble_data['lgb'].predict_proba(X)[0, 1]
        p_knn = ensemble_data['knn'].predict_proba(X)[0, 1]
        forecast_prob = (0.7 * p_lgb) + (0.3 * p_knn)
        
        prediction_result = {
            "probability": forecast_prob,
            "solexs_cps": row['solexs_sdd2_ctr'],
            "timestamp": current_time.isoformat()
        }
        
        # 2. Evaluate through the Decision Engine (handles Fallback, Alerts, Drift, Confidence, Recommendations)
        context = decision_engine.evaluate(prediction_result, telemetry_features=features_dict, current_time=current_time)
        
        # 3. Log to structured JSON decision logger
        decision_logger.info(f"Evaluated state: {context['operational_state']}", extra={"context": context})
        
        # Verbose terminal output for demonstration
        if context['operational_state'] in ["ALERT", "HIGH ALERT", "PRE-ALERT"]:
            logger.warning(f"[{current_time.strftime('%H:%M:%S')}] 🚨 {context['operational_state']} | {context['action_recommended']}")
        else:
            logger.info(f"[{current_time.strftime('%H:%M:%S')}] {context['operational_state']} | Prob: {forecast_prob:.2f} | Health: {context['telemetry_health']}")
            
        time.sleep(poll_interval_sec)

if __name__ == "__main__":
    run_daemon()
