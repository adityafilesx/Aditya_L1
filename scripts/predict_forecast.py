import os
import sys
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

# Add the project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))
from aditya_flare.processing.features import extract_features

def plot_forecast_timeline():
    processed_dir = Path("data/processed")
    model_path = Path("data/models/ensemble_forecaster.pkl")
    
    if not model_path.exists():
        print("Model file not found!")
        return

    print("Loading ensemble model...")
    with open(model_path, "rb") as f:
        ensemble_data = pickle.load(f)
    
    lgb_model = ensemble_data['lgb']
    knn_model = ensemble_data['knn']
    feature_cols = ensemble_data['features']
    
    print("Loading data for visualization (Extracting features)...")
    # Load 5 days of data for quick feature extraction
    df = extract_features(processed_dir, max_days=5, flare_threshold=500.0)
    
    # Check if we have a flare in this sample
    max_flare_idx = df['solexs_sdd2_ctr'].idxmax()
    if df.loc[max_flare_idx, 'solexs_sdd2_ctr'] < 500:
        print("No massive flare found in the first 5 days. Trying to load the whole dataset... this might take a minute.")
        df = extract_features(processed_dir, flare_threshold=500.0)
        max_flare_idx = df['solexs_sdd2_ctr'].idxmax()
    
    # We will pick a 12-hour window around the biggest flare
    start_time = max_flare_idx - pd.Timedelta(hours=4)
    end_time = max_flare_idx + pd.Timedelta(hours=4)
    
    window_df = df.loc[start_time:end_time].copy()
    
    print("Predicting 15-minute forecasting probabilities...")
    # Make sure we only use the exact features the model was trained on
    X_sim = window_df[feature_cols].values
    
    # Ensemble soft voting
    p_lgb = lgb_model.predict_proba(X_sim)[:, 1]
    p_knn = knn_model.predict_proba(X_sim)[:, 1]
    y_prob = (0.7 * p_lgb) + (0.3 * p_knn)
    
    window_df['forecast_prob'] = y_prob
    
    print("Plotting results...")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    
    # Top Plot: X-Ray Flux
    ax1.plot(window_df.index, window_df['solexs_sdd2_ctr'], color='blue', label='SoLEXS Soft X-Ray Flux')
    ax1.axhline(y=500, color='red', linestyle='--', label='C-Class Flare Threshold (500 counts/s)')
    ax1.set_ylabel('Counts / sec')
    ax1.set_title(f'Aditya-L1 SoLEXS Telemetry ({start_time.strftime("%Y-%m-%d")})')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # Bottom Plot: Ensemble Forecast Probability
    ax2.plot(window_df.index, window_df['forecast_prob'], color='purple', label='Ensemble Forecast Probability (15m Horizon)')
    ax2.axhline(y=0.5, color='orange', linestyle='--', label='50% Warning Threshold')
    
    # Highlight areas where prediction > 50%
    ax2.fill_between(window_df.index, window_df['forecast_prob'], 0.5, 
                     where=(window_df['forecast_prob'] >= 0.5), color='red', alpha=0.3)
                     
    ax2.set_ylabel('Probability')
    ax2.set_title('LightGBM + kNN Ensemble Forecast')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xlabel('UTC Time')
    
    plt.tight_layout()
    
    artifact_dir = "/Users/aditya1981/.gemini/antigravity-ide/brain/ead5211d-dfba-45f4-a3a2-adaf18c4ec59"
    plot_path = os.path.join(artifact_dir, "ensemble_forecast_timeline.png")
    plt.savefig(plot_path)
    print(f"Saved forecast timeline to: {plot_path}")

if __name__ == "__main__":
    plot_forecast_timeline()
