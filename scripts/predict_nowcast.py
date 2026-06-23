import os
import sys
from pathlib import Path
import xgboost as xgb
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Add the project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from aditya_flare.models.dataset import load_and_prepare_dataset, get_train_test_split

def plot_nowcast_timeline():
    processed_dir = Path("data/processed")
    print("Loading data for visualization...")
    df = load_and_prepare_dataset(processed_dir, target_threshold=500, horizon_minutes=15)
    
    X_train, X_test, y_train, y_test = get_train_test_split(df, test_size=0.2)
    
    print("Training XGBoost (Quick run for prediction)...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='auc',
        random_state=42
    )
    model.fit(X_train, y_train)
    
    print("Predicting probabilities on the Test Set...")
    # Get flare probability for the test set
    y_prob = model.predict_proba(X_test)[:, 1]
    
    # We will pick a 2-day window from the test set where there is high activity
    # Let's just find the max flare in the test set and plot 1 day around it
    test_df = df.iloc[len(X_train):].copy()
    test_df['flare_prob'] = y_prob
    
    max_flare_idx = test_df['solexs_sdd2_ctr'].idxmax()
    start_time = max_flare_idx - pd.Timedelta(hours=12)
    end_time = max_flare_idx + pd.Timedelta(hours=12)
    
    window_df = test_df.loc[start_time:end_time]
    
    if len(window_df) == 0:
        # Fallback to just plotting the first 24 hours of test set
        window_df = test_df.iloc[:60*24]
        
    print(f"Plotting timeline for: {window_df.index[0]} to {window_df.index[-1]}")
    
    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    
    # Top Plot: Actual X-ray Flux
    ax1.plot(window_df.index, window_df['solexs_sdd2_ctr'], color='blue', label='SoLEXS SDD2 (Soft X-rays)')
    ax1.axhline(500, color='red', linestyle='--', label='Flare Threshold (500 counts/s)')
    ax1.set_ylabel('Counts / sec')
    ax1.set_title('Aditya-L1 SoLEXS Actual X-Ray Flux')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    
    # Bottom Plot: Predicted Probability of Flare in Next 15 mins
    ax2.plot(window_df.index, window_df['flare_prob'], color='darkorange', label='Predicted Flare Probability (Next 15 min)')
    ax2.axhline(0.5, color='gray', linestyle='--', label='Decision Boundary (50%)')
    ax2.fill_between(window_df.index, 0, window_df['flare_prob'], color='darkorange', alpha=0.3)
    ax2.set_ylabel('Probability')
    ax2.set_xlabel('Time (UTC)')
    ax2.set_title('XGBoost Nowcasting Prediction (15-Minute Horizon)')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    # Format dates
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\\n%m-%d'))
    plt.tight_layout()
    
    artifact_dir = "/Users/aditya1981/.gemini/antigravity-ide/brain/db247a25-938f-4041-9c38-4920d6c3682f"
    plot_path = os.path.join(artifact_dir, "nowcast_timeline.png")
    plt.savefig(plot_path)
    print(f"Timeline plot saved to {plot_path}")

if __name__ == "__main__":
    plot_nowcast_timeline()
