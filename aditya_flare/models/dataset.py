import pandas as pd
import numpy as np
from pathlib import Path

def load_and_prepare_dataset(processed_dir, max_days=None, target_threshold=500, horizon_minutes=15):
    """
    Loads processed parquet files, resamples to 1-minute cadence to reduce noise 
    and dimensionality, builds sliding window features, and defines the binary target.
    """
    processed_dir = Path(processed_dir)
    parquet_files = sorted(list(processed_dir.glob("merged_*.parquet")))
    
    if max_days:
        parquet_files = parquet_files[:max_days]
        
    print(f"Loading {len(parquet_files)} daily parquet files...")
    dfs = []
    for f in parquet_files:
        df = pd.read_parquet(f)
        dfs.append(df)
        
    if not dfs:
        raise ValueError("No parquet files found!")
        
    full_df = pd.concat(dfs)
    # Ensure datetime index is sorted
    full_df = full_df.sort_index()
    
    # 1. Resample to 1-minute cadence (reduces 15M rows to ~250k rows)
    # Use mean for counts and hardness ratio. Bitmask can just take max.
    print("Resampling to 1-minute cadence...")
    agg_funcs = {
        'solexs_sdd2_ctr': 'mean',
        'helios_czt_broad_ctr': 'mean',
        'hardness_ratio': 'mean',
        'data_quality': 'max'
    }
    # Only keep valid columns that exist
    agg_cols = {k: v for k, v in agg_funcs.items() if k in full_df.columns}
    
    df_min = full_df.resample('1min').agg(agg_cols)
    
    # 2. Build Sliding Window Features
    print("Building physics features...")
    # Feature: Hardness Ratio Derivative (Change over 5 minutes)
    df_min['hr_diff_5m'] = df_min['hardness_ratio'].diff(periods=5)
    
    # Feature: Rolling Means to capture momentum
    df_min['hr_roll_mean_10m'] = df_min['hardness_ratio'].rolling(10).mean()
    df_min['solexs_roll_mean_10m'] = df_min['solexs_sdd2_ctr'].rolling(10).mean()
    
    # Feature: Recent max spikes
    df_min['czt_roll_max_5m'] = df_min['helios_czt_broad_ctr'].rolling(5).max()
    
    # 3. Define the Target (Classification)
    # Target: Will the SoLEXS count rate exceed `target_threshold` in the next `horizon_minutes`?
    print(f"Defining target: SoLEXS > {target_threshold} counts/sec in next {horizon_minutes} mins")
    
    # Calculate the max future value in the specified horizon
    # shift(-horizon) brings future values back, rolling looks backwards from there.
    # We use a trick: shift data by -1 (next minute) then do a rolling max of 'horizon_minutes' looking forward.
    future_max = df_min['solexs_sdd2_ctr'].shift(-1)[::-1].rolling(horizon_minutes, min_periods=1).max()[::-1]
    
    df_min['target_flare_in_horizon'] = (future_max > target_threshold).astype(int)
    
    # Drop NaNs created by rolling windows and target shifting
    df_min = df_min.dropna()
    
    # Only keep rows where original 1-min data was high quality (data_quality == 3 usually, or just not NaN)
    # For now, we rely on dropna() which removes intervals where instruments were off.
    
    print(f"Dataset ready! Total 1-min samples: {len(df_min)}")
    print(f"Target distribution (1=Flare): \\n{df_min['target_flare_in_horizon'].value_counts(normalize=True)*100}")
    
    return df_min

def get_train_test_split(df, test_size=0.2):
    """
    Splits the dataset chronologically (Time-Series split)
    """
    split_idx = int(len(df) * (1 - test_size))
    
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    features = [
        'solexs_sdd2_ctr', 'helios_czt_broad_ctr', 'hardness_ratio',
        'hr_diff_5m', 'hr_roll_mean_10m', 'solexs_roll_mean_10m', 'czt_roll_max_5m'
    ]
    target = 'target_flare_in_horizon'
    
    X_train = train_df[features]
    y_train = train_df[target]
    X_test = test_df[features]
    y_test = test_df[target]
    
    return X_train, X_test, y_train, y_test
