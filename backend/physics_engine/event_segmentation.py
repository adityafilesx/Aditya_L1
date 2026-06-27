import numpy as np
import pandas as pd
from backend.physics_engine.morphology import classify_morphology, detect_timeline_stage

def segment_events_and_timeline(df: pd.DataFrame, flux_col='solexs_sdd2_ctr', threshold=100.0) -> pd.DataFrame:
    """
    Segments flares dynamically and assigns timeline/morphology features.
    """
    out_df = df.copy()
    
    in_flare = False
    flare_start_idx = 0
    current_peak_val = 0.0
    current_peak_idx = 0
    
    fluxes = out_df[flux_col].values
    derivatives = np.gradient(fluxes)
    
    flare_starts = np.zeros(len(fluxes), dtype=int)
    flare_peaks = np.zeros(len(fluxes), dtype=int)
    flare_active = np.zeros(len(fluxes), dtype=bool)
    
    for i, flux in enumerate(fluxes):
        if not in_flare and flux >= threshold:
            in_flare = True
            flare_start_idx = i
            current_peak_val = flux
            current_peak_idx = i
            
        if in_flare:
            if flux > current_peak_val:
                current_peak_val = flux
                current_peak_idx = i
                
            if flux < threshold * 0.5 and i - current_peak_idx > 5:
                # Flare ended
                in_flare = False
                
        flare_starts[i] = flare_start_idx if in_flare else -1
        flare_peaks[i] = current_peak_idx if in_flare else -1
        flare_active[i] = in_flare
        
    out_df['is_flare_active'] = flare_active
    out_df['current_flare_peak'] = [fluxes[p] if p != -1 else 0 for p in flare_peaks]
    
    # Timeline
    timeline_stages = []
    for i in range(len(fluxes)):
        if not flare_active[i]:
            timeline_stages.append("Background")
        else:
            p_idx = flare_peaks[i]
            time_since_peak = i - p_idx
            
            stage = detect_timeline_stage(
                fluxes[i], 
                fluxes[p_idx], 
                derivatives[i], 
                time_since_peak if fluxes[i] < fluxes[p_idx] * 0.99 else 0, 
                True
            )
            timeline_stages.append(stage)
            
    out_df['physics_timeline'] = timeline_stages
    
    # Morphology
    morphs = []
    for i in range(len(fluxes)):
        if not flare_active[i]:
            morphs.append("None")
        else:
            s_idx = flare_starts[i]
            p_idx = flare_peaks[i]
            rise = p_idx - s_idx if p_idx >= s_idx else i - s_idx
            decay = i - p_idx if i > p_idx else 0
            m = classify_morphology(rise, decay, fluxes[p_idx])
            morphs.append(m)
            
    out_df['flare_morphology'] = morphs
    
    return out_df
