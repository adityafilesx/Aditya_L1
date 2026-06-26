import numpy as np
import pandas as pd
from scipy.stats import pearsonr

def compute_neupert_score(soft_flux_window, hard_flux_window):
    """
    Neupert Effect: Hard X-ray flux is proportional to the derivative of Soft X-ray flux.
    Score is the Pearson correlation between HXR and d(SXR)/dt.
    """
    if len(soft_flux_window) < 3:
        return 0.0
        
    # Calculate derivative of soft flux
    d_soft = np.gradient(soft_flux_window)
    
    # Calculate correlation
    if np.var(d_soft) < 1e-10 or np.var(hard_flux_window) < 1e-10:
        return 0.0
        
    r, _ = pearsonr(d_soft, hard_flux_window)
    return r

def extract_neupert_features(df: pd.DataFrame, soft_col='solexs_sdd2_ctr', hard_col='helios_czt_broad_ctr', window: int=15) -> pd.DataFrame:
    out_df = df.copy()
    
    if soft_col in out_df.columns and hard_col in out_df.columns:
        def neupert_wrapper(idx):
            start = max(0, idx - window + 1)
            end = idx + 1
            if end - start < 3: return 0.0
            return compute_neupert_score(
                out_df[soft_col].values[start:end],
                out_df[hard_col].values[start:end]
            )
            
        out_df['neupert_score'] = [neupert_wrapper(i) for i in range(len(out_df))]
        
    return out_df
