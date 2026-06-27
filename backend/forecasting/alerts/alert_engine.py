from typing import Dict, Any

class AlertEngine:
    """Escalates alerts (GREEN, YELLOW, ORANGE, RED, CRITICAL)."""
    
    def __init__(self):
        pass
        
    def get_alert_level(self, state: str) -> str:
        level = "GREEN"
        if state == "QUIET":
            level = "GREEN"
        elif state == "WATCH":
            level = "YELLOW"
        elif state == "WARNING":
            level = "ORANGE"
        elif state == "ALERT":
            level = "RED"
        elif state == "RECOVERY":
            level = "YELLOW"
        return level

alert_engine = AlertEngine()
