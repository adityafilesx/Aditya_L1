import numpy as np
import pandas as pd
from scipy.signal import periodogram, welch

def compute_spectral_features(x, fs=1.0):
    if len(x) < 4:
        return 0.0, 0.0, 0.0, 0.0
        
    f, psd = periodogram(x, fs)
    
    # Exclude DC component
    f = f[1:]
    psd = psd[1:]
    
    if np.sum(psd) == 0:
        return 0.0, 0.0, 0.0, 0.0
        
    # Spectral Centroid
    centroid = np.sum(f * psd) / np.sum(psd)
    
    # Spectral Flatness (Geometric Mean / Arithmetic Mean)
    # Adding small epsilon to avoid log(0)
    eps = 1e-10
    geom_mean = np.exp(np.mean(np.log(psd + eps)))
    arith_mean = np.mean(psd)
    flatness = geom_mean / arith_mean if arith_mean > 0 else 0.0
    
    # Spectral Roll-off (85%)
    cum_sum = np.cumsum(psd)
    roll_off_idx = np.where(cum_sum >= 0.85 * cum_sum[-1])[0][0]
    roll_off = f[roll_off_idx]
    
    # Dominant Oscillation (Frequency with max power)
    dominant_freq = f[np.argmax(psd)]
    
    return centroid, flatness, roll_off, dominant_freq

def extract_spectral_features(df: pd.DataFrame, columns: list, window: int = 15) -> pd.DataFrame:
    out_df = df.copy()
    
    for col in columns:
        if col not in df.columns:
            continue
            
        def spec_wrapper(x):
            c, f, r, d = compute_spectral_features(x)
            return c
            
        # Due to pandas rolling apply returning a single scalar, we extract each separately
        # To optimize, we can do this in a single loop if speed becomes an issue,
        # but window=15 is very small, so apply is fast.
        
        roll = df[col].rolling(window, min_periods=window)
        
        out_df[f'{col}_spec_centroid_{window}'] = roll.apply(lambda x: compute_spectral_features(x)[0], raw=True).fillna(0)
        out_df[f'{col}_spec_flatness_{window}'] = roll.apply(lambda x: compute_spectral_features(x)[1], raw=True).fillna(0)
        out_df[f'{col}_spec_rolloff_{window}'] = roll.apply(lambda x: compute_spectral_features(x)[2], raw=True).fillna(0)
        out_df[f'{col}_dominant_freq_{window}'] = roll.apply(lambda x: compute_spectral_features(x)[3], raw=True).fillna(0)
        
    return out_df
