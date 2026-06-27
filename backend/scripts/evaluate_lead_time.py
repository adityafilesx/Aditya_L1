import os
import sys
import json
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))
from backend.aditya_flare.processing.features import extract_features

def evaluate_lead_time():
    print("Evaluating Ensemble Model Lead Time & Verification Metrics...")
    
    processed_dir = Path("data/processed")
    model_path = Path("data/models/ensemble_forecaster.pkl")
    catalog_path = processed_dir / "master_flare_catalog.csv"
    metrics_out = processed_dir / "lead_time_metrics.json"
    plot_out = processed_dir / "lead_time_distribution.png"
    
    if not model_path.exists() or not catalog_path.exists():
        print("Error: Missing model or master catalog.")
        return
        
    with open(model_path, "rb") as f:
        ensemble_data = pickle.load(f)
        
    print("Extracting features over entire dataset (this may take a minute)...")
    # We extract all available features (pass max_days=None)
    df = extract_features(processed_dir, flare_threshold=500.0)
    
    print("Generating predictions...")
    X_test = df[ensemble_data['features']].values
    p_lgb = ensemble_data['lgb'].predict_proba(X_test)[:, 1]
    p_knn = ensemble_data['knn'].predict_proba(X_test)[:, 1]
    df['forecast_prob'] = (0.7 * p_lgb) + (0.3 * p_knn)
    
    # Identify flares from the catalog
    catalog_df = pd.read_csv(catalog_path)
    for col in ['start_time', 'end_time', 'peak_time_soft', 'peak_time_hard']:
        if col in catalog_df.columns:
            catalog_df[col] = pd.to_datetime(catalog_df[col], errors='coerce').dt.tz_localize('UTC')
            
    # Lead time calculation
    lead_times = []
    true_positives = 0
    false_negatives = 0
    
    for _, flare in catalog_df.iterrows():
        peak = flare['peak_time_soft']
        if pd.isna(peak):
            peak = flare['peak_time_hard']
        if pd.isna(peak):
            peak = flare['start_time'] + pd.Timedelta(minutes=5)
            
        start_search = flare['start_time'] - pd.Timedelta(minutes=60)
        end_search = peak
        
        # Get data slice
        slice_df = df.loc[(df.index >= start_search) & (df.index <= end_search)]
        
        # Find first trigger
        triggers = slice_df[slice_df['forecast_prob'] > 0.70]
        
        if not triggers.empty:
            trigger_time = triggers.index[0]
            # Ensure trigger happens before peak
            if trigger_time < peak:
                lead_time = (peak - trigger_time).total_seconds() / 60.0
                lead_times.append(lead_time)
                true_positives += 1
            else:
                false_negatives += 1
        else:
            false_negatives += 1
            
    # Calculate False Alarm Rate (FAR)
    # A false alarm is a block of contiguous predictions > 0.70 that are NOT within 60 mins of any flare
    # To simplify, we find all points where prob > 0.70
    all_triggers = df[df['forecast_prob'] > 0.70]
    
    false_alarms = 0
    # Create an array of safe regions
    df['in_flare_window'] = False
    for _, flare in catalog_df.iterrows():
        start = flare['start_time'] - pd.Timedelta(minutes=60)
        end = flare['end_time'] + pd.Timedelta(minutes=60)
        df.loc[(df.index >= start) & (df.index <= end), 'in_flare_window'] = True
        
    fa_triggers = all_triggers[~df.loc[all_triggers.index, 'in_flare_window']]
    
    # Cluster FA triggers into distinct events (e.g. gap > 30 mins)
    if not fa_triggers.empty:
        fa_times = fa_triggers.index
        time_diffs = fa_times.to_series().diff().dt.total_seconds() / 60.0
        # Number of contiguous false alarm blocks
        false_alarms = 1 + (time_diffs > 30).sum()
        
    tpr = (true_positives / (true_positives + false_negatives)) * 100 if (true_positives + false_negatives) > 0 else 0
    # FAR = FA / (TP + FA)
    far = (false_alarms / (true_positives + false_alarms)) * 100 if (true_positives + false_alarms) > 0 else 0
    avg_lead_time = np.mean(lead_times) if lead_times else 0.0
    
    metrics = {
        "true_positives": true_positives,
        "false_negatives": false_negatives,
        "false_alarms": int(false_alarms),
        "tpr_percent": float(tpr),
        "far_percent": float(far),
        "avg_lead_time_min": float(avg_lead_time)
    }
    
    with open(metrics_out, "w") as f:
        json.dump(metrics, f, indent=4)
        
    print(f"\\n--- Verification Results ---")
    print(f"True Positives: {true_positives}")
    print(f"False Negatives (Missed): {false_negatives}")
    print(f"False Alarms (Quiet Sun Triggers): {false_alarms}")
    print(f"TPR: {tpr:.1f}%")
    print(f"FAR: {far:.1f}%")
    print(f"Average Lead Time: {avg_lead_time:.1f} minutes")
    print(f"Metrics saved to {metrics_out}")
    
    # Plotting the distribution
    if lead_times:
        plt.figure(figsize=(8, 5))
        plt.hist(lead_times, bins=20, color='skyblue', edgecolor='black')
        plt.axvline(avg_lead_time, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {avg_lead_time:.1f} min')
        plt.title('Distribution of Predictive Lead Times')
        plt.xlabel('Lead Time (Minutes before Peak)')
        plt.ylabel('Frequency (Number of Flares)')
        plt.legend()
        plt.grid(axis='y', alpha=0.5)
        plt.savefig(plot_out)
        print(f"Distribution plot saved to {plot_out}")

if __name__ == '__main__':
    evaluate_lead_time()
