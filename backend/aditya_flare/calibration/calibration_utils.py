import numpy as np

def flux_to_goes_class_string(flux_w_m2: float) -> str:
    """
    Converts GOES flux in W/m^2 to standard GOES class string (e.g. M3.2).
    """
    if flux_w_m2 <= 0 or np.isnan(flux_w_m2):
        return "Unknown"
        
    if flux_w_m2 >= 1e-4:
        goes_class = 'X'
        multiplier = flux_w_m2 / 1e-4
    elif flux_w_m2 >= 1e-5:
        goes_class = 'M'
        multiplier = flux_w_m2 / 1e-5
    elif flux_w_m2 >= 1e-6:
        goes_class = 'C'
        multiplier = flux_w_m2 / 1e-6
    elif flux_w_m2 >= 1e-7:
        goes_class = 'B'
        multiplier = flux_w_m2 / 1e-7
    else:
        goes_class = 'A'
        multiplier = flux_w_m2 / 1e-8

    return f"{goes_class}{multiplier:.1f}"

def parse_goes_class_string(class_str: str) -> float:
    """
    Converts GOES class string back to flux in W/m^2.
    """
    if not class_str or len(class_str) < 2:
        return np.nan
        
    letter = class_str[0].upper()
    try:
        multiplier = float(class_str[1:])
    except ValueError:
        return np.nan
        
    mapping = {'X': 1e-4, 'M': 1e-5, 'C': 1e-6, 'B': 1e-7, 'A': 1e-8}
    if letter not in mapping:
        return np.nan
        
    return mapping[letter] * multiplier
