import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import linregress

def extract_features(processed_dir: str, max_days: int = None, flare_threshold: float = 500.0) -> pd.DataFrame:
    """
    Loads parquet files, resamples to 1-minute cadence, and builds robust temporal,
    volatility, and Nishizuka historical features.
    
    Args:
        processed_dir: Path to the processed directory containing parquet files.
        max_days: Limit number of days to load (for testing).
        flare_threshold: The count rate threshold to define a flare event.
        
    Returns:
        pd.DataFrame: Feature matrix ready for ML training.
    """
    processed_dir = Path(processed_dir)
    parquet_files = sorted(list(processed_dir.glob("merged_*.parquet")))
    
    if max_days:
        parquet_files = parquet_files[:max_days]
        
    print(f"Loading {len(parquet_files)} parquet files...")
    dfs = [pd.read_parquet(f) for f in parquet_files]
    
    if not dfs:
        raise ValueError("No parquet files found!")
        
    full_df = pd.concat(dfs).sort_index()
    
    # --- 1. Resampling to 1-minute cadence ---
    print("Resampling to 1-minute cadence...")
    agg_funcs = {
        'solexs_sdd2_ctr': 'mean',
        'helios_czt_broad_ctr': 'mean',
        'hardness_ratio': 'mean'
    }
    agg_cols = {k: v for k, v in agg_funcs.items() if k in full_df.columns}
    df = full_df.resample('1min').agg(agg_cols).interpolate(method='linear', limit=30).ffill()
    
    # Helper for fast rolling slope
    def rolling_slope(series, window):
        # Slope = Cov(x, y) / Var(x)
        # x is just a linear sequence 0, 1, 2...
        x = np.arange(window)
        x_mean = np.mean(x)
        x_var = np.var(x)
        
        def slope_func(y):
            if np.isnan(y).any():
                return np.nan
            y_mean = np.mean(y)
            cov = np.mean((x - x_mean) * (y - y_mean))
            return cov / x_var if x_var > 0 else 0.0
            
        return series.rolling(window).apply(slope_func, raw=True)

    print("Extracting Temporal Gradients (Slopes)...")
    for col in ['solexs_sdd2_ctr', 'helios_czt_broad_ctr', 'hardness_ratio']:
        if col in df.columns:
            df[f'{col}_slope_3m'] = rolling_slope(df[col], 3)
            df[f'{col}_slope_5m'] = rolling_slope(df[col], 5)
            df[f'{col}_slope_15m'] = rolling_slope(df[col], 15)

    print("Extracting Volatility Metrics...")
    for col in ['solexs_sdd2_ctr', 'helios_czt_broad_ctr']:
        if col in df.columns:
            df[f'{col}_std_5m'] = df[col].rolling(5).std()
            df[f'{col}_var_5m'] = df[col].rolling(5).var()
            df[f'{col}_std_30m'] = df[col].rolling(30).std()
            df[f'{col}_var_30m'] = df[col].rolling(30).var()

    print("Simulating Nishizuka Flare History Features...")
    # Define flare flag
    df['is_flare'] = (df['solexs_sdd2_ctr'] >= flare_threshold).astype(int)
    
    # Count of flares in past 1h (60m), 6h (360m), 24h (1440m)
    df['flares_past_1h'] = df['is_flare'].rolling(60, closed='left').sum().fillna(0)
    df['flares_past_6h'] = df['is_flare'].rolling(360, closed='left').sum().fillna(0)
    df['flares_past_24h'] = df['is_flare'].rolling(1440, closed='left').sum().fillna(0)
    
    # Time since last flare and max peak intensity of last flare
    # This requires an iterative or efficient cumulative approach
    time_since_last = []
    last_peak_intensity = []
    
    current_time_since = 9999.0 # Large default
    current_peak = 0.0
    is_in_flare = False
    
    # We iterate over the series. For 250k rows, Python iteration is ~1-2 seconds.
    flux_values = df['solexs_sdd2_ctr'].values
    is_flare_values = df['is_flare'].values
    
    for i in range(len(flux_values)):
        flux = flux_values[i]
        flare = is_flare_values[i]
        
        # Append before updating state to prevent data leakage!
        # Features at time t must only use data from <= t (actually < t for historical peak)
        time_since_last.append(current_time_since)
        last_peak_intensity.append(current_peak)
        
        if flare == 1:
            if not is_in_flare:
                is_in_flare = True
                current_peak = flux
            else:
                current_peak = max(current_peak, flux)
            current_time_since = 0.0
        else:
            is_in_flare = False
            current_time_since += 1.0 # 1 minute elapsed
            
    df['time_since_last_flare_m'] = time_since_last
    df['last_flare_peak_intensity'] = last_peak_intensity
    
    # Note: phys_temp, phys_em, phys_photon_index are skipped gracefully since they aren't merged yet
    
    # Drop intermediate column used for simulation
    # df.drop(columns=['is_flare'], inplace=True)
    
    # Drop early NaNs caused by rolling windows
    df = df.dropna()
    print(f"Feature Extraction Complete. Matrix shape: {df.shape}")
    
    return df
