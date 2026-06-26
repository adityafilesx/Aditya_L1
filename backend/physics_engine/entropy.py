import numpy as np
import pandas as pd
from scipy.signal import periodogram

def shannon_entropy(x):
    # Digitize to compute discrete probabilities
    hist, _ = np.histogram(x, bins='fd')
    p = hist / np.sum(hist)
    p = p[p > 0]
    return -np.sum(p * np.log2(p))

def sample_entropy(x, m=2, r=0.2):
    # Approximation of sample entropy for real-time
    x = np.asarray(x)
    n = len(x)
    if n <= m + 1: return 0.0
    
    r *= np.std(x)
    
    def _phi(m):
        x_m = np.array([x[i:i+m] for i in range(n - m + 1)])
        C = 0
        for i in range(len(x_m)):
            dist = np.max(np.abs(x_m - x_m[i]), axis=1)
            C += np.sum(dist <= r) - 1 # exclude self
        return C / (len(x_m) * (len(x_m) - 1)) if len(x_m) > 1 else 1e-10
        
    phi_m = _phi(m)
    phi_m1 = _phi(m + 1)
    
    if phi_m == 0 or phi_m1 == 0:
        return 0.0
    return -np.log(phi_m1 / phi_m)

def spectral_entropy(x, fs=1.0):
    if len(x) < 2: return 0.0
    _, psd = periodogram(x, fs)
    psd_norm = psd / np.sum(psd)
    psd_norm = psd_norm[psd_norm > 0]
    return -np.sum(psd_norm * np.log2(psd_norm))

def extract_entropy_features(df: pd.DataFrame, columns: list, window: int = 15) -> pd.DataFrame:
    out_df = df.copy()
    
    for col in columns:
        if col not in df.columns:
            continue
            
        roll = df[col].rolling(window, min_periods=window)
        
        # Shannon Entropy
        out_df[f'{col}_shannon_entropy_{window}'] = roll.apply(shannon_entropy, raw=True).fillna(0)
        
        # Sample Entropy (computationally expensive, using a smaller window or subsampled proxy if needed, but we'll run it)
        # For real-time <100ms, Sample Entropy on window=15 is very fast (N=15 is tiny).
        out_df[f'{col}_sample_entropy_{window}'] = roll.apply(lambda x: sample_entropy(x, m=2, r=0.2), raw=True).fillna(0)
        
        # Spectral Entropy
        out_df[f'{col}_spectral_entropy_{window}'] = roll.apply(lambda x: spectral_entropy(x), raw=True).fillna(0)
        
    return out_df
