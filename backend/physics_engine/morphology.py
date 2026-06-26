import numpy as np
import pandas as pd

def classify_morphology(rise_time, decay_time, peak_flux):
    """
    Classify Flare Morphology based on times and intensity.
    """
    if peak_flux < 50:
        return "Microflare"
        
    duration = rise_time + decay_time
    
    if duration > 120: # Long Duration Event
        return "Long Duration Event"
        
    if rise_time < 10 and decay_time < 30:
        return "Impulsive"
        
    if rise_time >= 10 or decay_time >= 30:
        return "Gradual"
        
    return "Complex"

def detect_timeline_stage(current_flux, peak_flux, derivative, time_since_peak, is_flare_active):
    """
    Returns the current physics timeline stage.
    """
    if not is_flare_active:
        return "Background"
        
    if time_since_peak < 0: # Pre-peak
        if current_flux < 0.1 * peak_flux and derivative > 0:
            return "Preheating"
        elif derivative > 5: # Fast rise
            return "Impulsive Rise"
        else:
            return "Early Rise"
    elif time_since_peak == 0:
        return "Peak"
    else: # Post-peak
        if current_flux > 0.5 * peak_flux:
            return "Early Decay"
        elif current_flux > 0.1 * peak_flux:
            return "Late Decay"
        else:
            return "Recovery"


