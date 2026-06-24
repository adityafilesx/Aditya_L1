import os
import glob
import pandas as pd
import numpy as np
from pathlib import Path
from astropy.io import fits

def extract_suit_features(suit_dir):
    """
    Scans the suit directory for FITS files, extracts the timestamp
    and mean/max intensities, and returns a DataFrame indexed by time.
    """
    suit_dir = Path(suit_dir)
    fits_files = sorted(glob.glob(str(suit_dir / "*.fits")))
    
    records = []
    for f in fits_files:
        try:
            with fits.open(f) as hdul:
                data_idx = 0
                for idx, hdu in enumerate(hdul):
                    if hdu.data is not None and len(hdu.data.shape) == 2:
                        data_idx = idx
                        break
                header = hdul[data_idx].header
                data = hdul[data_idx].data
                
                date_obs = header.get('DATE-OBS')
                if date_obs:
                    dt_str = date_obs.replace('Z', '').split('+')[0]
                    dt = pd.to_datetime(dt_str)
                    if dt.tz is None:
                        dt = dt.tz_localize('UTC')
                    else:
                        dt = dt.tz_convert('UTC')
                    
                    mean_val = float(np.mean(data))
                    max_val = float(np.max(data))
                    
                    records.append({
                        'timestamp': dt,
                        'suit_uv_mean': mean_val,
                        'suit_uv_max': max_val
                    })
        except Exception as e:
            print(f"Error parsing FITS file {f}: {e}")
            
    if not records:
        return pd.DataFrame(columns=['suit_uv_mean', 'suit_uv_max'])
        
    df = pd.DataFrame(records)
    df = df.set_index('timestamp').sort_index()
    return df

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
    
    # 2. Extract and Merge SUIT UV Data
    suit_dir = processed_dir.parent / "raw" / "suit"
    print(f"Extracting SUIT features from {suit_dir}...")
    suit_df = extract_suit_features(suit_dir)
    
    if not suit_df.empty:
        print(f"Successfully loaded {len(suit_df)} SUIT images. Merging with 1-min cadence data...")
        df_min = df_min.sort_index()
        suit_df = suit_df.sort_index()
        
        df_min = pd.merge_asof(
            df_min,
            suit_df,
            left_index=True,
            right_index=True,
            direction='backward'
        )
        
        df_min['suit_uv_mean'] = df_min['suit_uv_mean'].ffill().bfill()
        df_min['suit_uv_max'] = df_min['suit_uv_max'].ffill().bfill()
        
        # Fallback if no temporal overlap (e.g. 2026 SUIT file vs 2024 historical dataset)
        if df_min['suit_uv_mean'].isna().all():
            print("Warning: No temporal overlap between SUIT files and dataset. Filling with SUIT mean fallback values.")
            fallback_mean = suit_df['suit_uv_mean'].mean()
            fallback_max = suit_df['suit_uv_max'].mean()
            df_min['suit_uv_mean'] = df_min['suit_uv_mean'].fillna(fallback_mean)
            df_min['suit_uv_max'] = df_min['suit_uv_max'].fillna(fallback_max)
    else:
        print("Warning: No SUIT features found. Defaulting SUIT columns to 0.0.")
        df_min['suit_uv_mean'] = 0.0
        df_min['suit_uv_max'] = 0.0
        
    # 3. Build Sliding Window Features
    print("Building physics features...")
    # Feature: Hardness Ratio Derivative (Change over 5 minutes)
    df_min['hr_diff_5m'] = df_min['hardness_ratio'].diff(periods=5)
    
    # Feature: Rolling Means to capture momentum
    df_min['hr_roll_mean_10m'] = df_min['hardness_ratio'].rolling(10).mean()
    df_min['solexs_roll_mean_10m'] = df_min['solexs_sdd2_ctr'].rolling(10).mean()
    
    # Feature: Recent max spikes
    df_min['czt_roll_max_5m'] = df_min['helios_czt_broad_ctr'].rolling(5).max()
    
    # 4. Define the Target (Classification)
    # Target: Will the SoLEXS count rate exceed `target_threshold` in the next `horizon_minutes`?
    print(f"Defining target: SoLEXS > {target_threshold} counts/sec in next {horizon_minutes} mins")
    
    # Calculate the max future value in the specified horizon
    future_max = df_min['solexs_sdd2_ctr'].shift(-1)[::-1].rolling(horizon_minutes, min_periods=1).max()[::-1]
    
    df_min['target_flare_in_horizon'] = (future_max > target_threshold).astype(int)
    
    # Drop NaNs created by rolling windows and target shifting
    df_min = df_min.dropna()
    
    print(f"Dataset ready! Total 1-min samples: {len(df_min)}")
    print(f"Target distribution (1=Flare): \n{df_min['target_flare_in_horizon'].value_counts(normalize=True)*100}")
    
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
        'hr_diff_5m', 'hr_roll_mean_10m', 'solexs_roll_mean_10m', 'czt_roll_max_5m',
        'suit_uv_mean', 'suit_uv_max'
    ]
    target = 'target_flare_in_horizon'
    
    X_train = train_df[features]
    y_train = train_df[target]
    X_test = test_df[features]
    y_test = test_df[target]
    
    return X_train, X_test, y_train, y_test
