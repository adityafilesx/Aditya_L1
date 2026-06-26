import numpy as np
import pandas as pd
from scipy.stats import pearsonr

def estimate_thermodynamics(soft_flux, hard_flux):
    """
    Empirical fallback for Temperature (MK) and Emission Measure (norm)
    if XSPEC is unavailable. Based on hardness ratio.
    """
    # Prevent div by zero
    soft = np.maximum(soft_flux, 1e-8)
    hard = np.maximum(hard_flux, 1e-8)
    
    hr = hard / soft
    
    # Emission Measure estimation from HR is highly unreliable without spectral fitting.
    # User requested to return "not available" (NaN) unless validated model is present.
    temp_mk = np.clip(15.0 * np.sqrt(hr), 2.0, 50.0)
    em_norm = np.full_like(temp_mk, np.nan)
    confidence = np.zeros_like(temp_mk) # 0.0 confidence without XSPEC
    
    return temp_mk, em_norm, confidence

def extract_thermodynamic_features(df: pd.DataFrame, soft_col='solexs_sdd2_ctr', hard_col='helios_czt_broad_ctr', window: int=15) -> pd.DataFrame:
    out_df = df.copy()
    
    # Check if we have both fluxes
    if soft_col in out_df.columns and hard_col in out_df.columns:
        # 1. Temperature & EM
        T_mk, EM, conf = estimate_thermodynamics(out_df[soft_col].values, out_df[hard_col].values)
        out_df['estimated_temperature_mk'] = T_mk
        out_df['estimated_em_norm'] = EM
        out_df['thermo_confidence'] = conf
        
        # 2. Gradients (Heating / Cooling Rates)
        out_df['temperature_gradient'] = out_df['estimated_temperature_mk'].diff().fillna(0)
        out_df['em_gradient'] = out_df['estimated_em_norm'].diff().fillna(0)
        
        # Thermal Energy Proxy (E ~ 3 k_b T sqrt(EM * V))
        # Since EM is NaN, this will be NaN, which is physically correct.
        out_df['thermal_energy_proxy'] = out_df['estimated_temperature_mk'] * np.sqrt(out_df['estimated_em_norm'])
        
    return out_df
