import numpy as np
import pandas as pd
import pywt

def compute_wavelet_energy(x, wavelet='db4', level=2):
    if len(x) < 2**level:
        return 0.0
    coeffs = pywt.wavedec(x, wavelet, level=level)
    energy = sum(np.sum(np.square(c)) for c in coeffs)
    return energy

def dominant_scale_wpt(x, wavelet='db2', max_level=3):
    if len(x) < 2**max_level: return 0.0
    # Wavelet Packet Transform
    wp = pywt.WaveletPacket(data=x, wavelet=wavelet, mode='symmetric', maxlevel=max_level)
    
    # Calculate energy in each node at max_level
    nodes = wp.get_level(max_level, 'freq')
    energies = [np.sum(np.square(n.data)) for n in nodes]
    
    # Return the index of the node with max energy as a proxy for dominant scale/band
    dom_node_idx = np.argmax(energies)
    return float(dom_node_idx)

def extract_wavelet_features(df: pd.DataFrame, columns: list, window: int = 15) -> pd.DataFrame:
    out_df = df.copy()
    
    for col in columns:
        if col not in df.columns:
            continue
            
        roll = df[col].rolling(window, min_periods=window)
        
        # Wavelet Energy (Discrete)
        out_df[f'{col}_wavelet_energy_{window}'] = roll.apply(
            lambda x: compute_wavelet_energy(x, wavelet='db2', level=1), raw=True
        ).fillna(0)
        
        # Dominant Scale (WPT proxy)
        out_df[f'{col}_dominant_scale_{window}'] = roll.apply(
            lambda x: dominant_scale_wpt(x, wavelet='db2', max_level=3), raw=True
        ).fillna(0)
        
        # High Frequency Burst Detection (Microflare detection proxy)
        # Using the detail coefficients (D1) of DWT to represent high frequency bursts
        def burst_intensity(x):
            if len(x) < 2: return 0.0
            cA, cD = pywt.dwt(x, 'db2')
            return np.max(np.abs(cD))
            
        out_df[f'{col}_hf_burst_intensity_{window}'] = roll.apply(burst_intensity, raw=True).fillna(0)
        
    return out_df
