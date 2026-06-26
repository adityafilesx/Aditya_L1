class OperationalState:
    QUIET = "QUIET"
    WATCH = "WATCH"
    PRE_ALERT = "PRE-ALERT"
    ALERT = "ALERT"
    HIGH_ALERT = "HIGH ALERT"
    RECOVERY = "RECOVERY"

def parse_goes_class(goes_class_str: str) -> float:
    """Parses a GOES class string like 'X1.2' to a numerical flux value."""
    if not goes_class_str:
        return 0.0
    
    goes_class_str = goes_class_str.strip().upper()
    if not goes_class_str:
        return 0.0
        
    letter = goes_class_str[0]
    try:
        multiplier = float(goes_class_str[1:]) if len(goes_class_str) > 1 else 1.0
    except ValueError:
        multiplier = 1.0
        
    exponents = {'A': 1e-8, 'B': 1e-7, 'C': 1e-6, 'M': 1e-5, 'X': 1e-4}
    base = exponents.get(letter, 1e-8)
    return base * multiplier
