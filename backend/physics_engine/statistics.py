import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis

def extract_statistical_features(df: pd.DataFrame, columns: list, window: int = 15) -> pd.DataFrame:
    """
    Extracts higher-order statistical moments and rolling features.
    Args:
        df: Input DataFrame.
        columns: List of columns to process.
        window: Rolling window size.
    Returns:
        DataFrame with added statistical features.
    """
    out_df = df.copy()
    
    for col in columns:
        if col not in df.columns:
            continue
            
        # Basic rolling stats
        roll = df[col].rolling(window, min_periods=1)
        out_df[f'{col}_roll_mean_{window}'] = roll.mean()
        out_df[f'{col}_roll_std_{window}'] = roll.std().fillna(0)
        out_df[f'{col}_roll_median_{window}'] = roll.median()
        out_df[f'{col}_roll_var_{window}'] = roll.var().fillna(0)
        
        # Median Absolute Deviation (MAD)
        def mad(x):
            return np.median(np.abs(x - np.median(x)))
        out_df[f'{col}_roll_mad_{window}'] = roll.apply(mad, raw=True)
        
        # Skewness and Kurtosis
        out_df[f'{col}_roll_skew_{window}'] = roll.apply(lambda x: skew(x, bias=False), raw=True).fillna(0)
        out_df[f'{col}_roll_kurtosis_{window}'] = roll.apply(lambda x: kurtosis(x, bias=False), raw=True).fillna(0)
        
        # Moving RMS
        out_df[f'{col}_roll_rms_{window}'] = roll.apply(lambda x: np.sqrt(np.mean(x**2)), raw=True)
        
        # Rolling Quantiles
        out_df[f'{col}_roll_q90_{window}'] = roll.quantile(0.90)
        
        # Peak Width / Peak Symmetry (approximations over window)
        # Symmetry: (Mean - Median) / Std
        std_col = out_df[f'{col}_roll_std_{window}']
        out_df[f'{col}_roll_symmetry_{window}'] = np.where(
            std_col > 0, 
            (out_df[f'{col}_roll_mean_{window}'] - out_df[f'{col}_roll_median_{window}']) / std_col, 
            0
        )
        
    return out_df
