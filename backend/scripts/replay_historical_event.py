import os
import sys
import argparse
import pandas as pd
import numpy as np
import xgboost as xgb
from pathlib import Path
from datetime import datetime

# Add the project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from backend.aditya_flare.config.config_loader import config
from backend.aditya_flare.decision.state_machine import DecisionEngine
from backend.aditya_flare.utils.logger import setup_logger

logger = setup_logger("ReplayEngine", "replay.log")

def replay_event(target_date_str: str):
    """
    Module 5: Historical Event Replay
    Simulates the real-time operational decision support system running chronologically 
    over a historical event.
    """
    logger.info(f"Initializing Historical Replay for: {target_date_str}")
    
    # Load dataset
    date_formatted = target_date_str.replace('-', '')
    processed_dir = Path(config.processed_dir)
    merged_file = processed_dir / f"merged_{date_formatted}.parquet"
    
    if not merged_file.exists():
        logger.error(f"Daily merged dataset not found at {merged_file}")
        return
        
    df = pd.read_parquet(merged_file)
    
    # Ensure time_utc is datetime
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        if 'time_utc' in df.columns:
            df['time_utc'] = pd.to_datetime(df['time_utc'])
            df.set_index('time_utc', inplace=True)
        else:
            logger.error("Dataset must have time_utc index or column.")
            return
            
    # Keep index in DatetimeIndex format
    df.index = pd.to_datetime(df.index, utc=True)
    df = df.sort_index()
    
    # Resample to 1-minute cadence to match the model's training cadence
    agg_funcs = {
        'solexs_sdd2_ctr': 'mean',
        'helios_czt_broad_ctr': 'mean',
        'hardness_ratio': 'mean'
    }
    agg_cols = {k: v for k, v in agg_funcs.items() if k in df.columns}
    event_df = df.resample('1min').agg(agg_cols).interpolate(method='linear', limit=10).ffill()
    
    if event_df.empty:
        logger.error(f"No data found for date {target_date_str}")
        return
        
    logger.info(f"Loaded {len(event_df)} 1-minute samples for {target_date_str}.")
    
    # Build features (to simulate the exact input the model sees)
    # Use .get() to avoid KeyError if a column is missing from the specific date's telemetry
    event_df['hr_diff_5m'] = event_df.get('hardness_ratio', pd.Series(0.0, index=event_df.index)).diff(periods=5).fillna(0)
    event_df['hr_roll_mean_10m'] = event_df.get('hardness_ratio', pd.Series(0.0, index=event_df.index)).rolling(10).mean().fillna(0)
    event_df['solexs_roll_mean_10m'] = event_df.get('solexs_sdd2_ctr', pd.Series(0.0, index=event_df.index)).rolling(10).mean().fillna(0)
    event_df['czt_roll_max_5m'] = event_df.get('helios_czt_broad_ctr', pd.Series(0.0, index=event_df.index)).rolling(5).max().fillna(0)
    event_df['suit_uv_mean'] = 0.0
    event_df['suit_uv_max'] = 0.0
    
    # Load Model
    models_dir = Path(config.models_dir)
    model_path = models_dir / "xgboost_nowcast.json"
    if not model_path.exists():
        logger.error(f"XGBoost model not found at {model_path}")
        return
        
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    
    # Expected features (from model)
    feature_names = model.get_booster().feature_names
    for f in feature_names:
        if f not in event_df.columns:
            logger.warning(f"Feature {f} missing, filling with 0")
            event_df[f] = 0.0
            
    X_replay = event_df[feature_names]
    
    # Initialize Decision Engine
    decision_engine = DecisionEngine()
    
    logger.info("--- BEGIN REPLAY ---")
    
    # Replay Chronologically
    transitions = []
    
    for i in range(len(event_df)):
        timestamp = event_df.index[i]
        row_features = X_replay.iloc[[i]]
        
        # In a real system, features are extracted from telemetry. Here we just take the row.
        
        # Handle NaNs
        if row_features.isna().any(axis=None):
            # Simulated telemetry gap
            health = "GAP"
            prob = 0.0
            flux_cps = 0.0
        else:
            health = "OK"
            prob = float(model.predict_proba(row_features)[0, 1])
            # Assuming solexs_sdd2_ctr is a feature
            flux_cps = float(event_df.iloc[i].get('solexs_sdd2_ctr', 0.0))
            
        prediction_result = {
            "timestamp": timestamp.isoformat(),
            "probability": prob,
            "solexs_cps": flux_cps,
            "estimated_goes_class": None # Will be estimated dynamically by the engine
        }
        
        telemetry_status = {"health": health}
        
        # Step through the State Machine
        eval_result = decision_engine.evaluate(prediction_result, telemetry_status)
        
        current_state = eval_result["operational_state"]
        prev_state = eval_result["previous_state"]
        
        # Log state transitions
        if current_state != prev_state:
            logger.info(f"[{timestamp.strftime('%H:%M:%S')}] STATE TRANSITION: {prev_state} -> {current_state}")
            logger.info(f"   Probability: {eval_result['probability']:.3f} | Flux: {eval_result['estimated_flux']:.1e} | Confidence: {eval_result['is_confident']}")
            logger.info(f"   Primary Action: {eval_result['action_recommended']}")
            
            transitions.append(eval_result)
            
    logger.info("--- END REPLAY ---")
    logger.info(f"Total state transitions recorded: {len(transitions)}")
    
    # Save replay log to evaluation directory
    if transitions:
        eval_dir = Path("data/evaluation/replays")
        eval_dir.mkdir(parents=True, exist_ok=True)
        out_file = eval_dir / f"replay_{target_date_str}.csv"
        pd.DataFrame(transitions).to_csv(out_file, index=False)
        logger.info(f"Saved transition log to {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Historical Event Replay for Decision Engine")
    parser.add_argument("--date", type=str, default="2024-02-12", help="Target date to replay (YYYY-MM-DD)")
    args = parser.parse_args()
    
    replay_event(args.date)
