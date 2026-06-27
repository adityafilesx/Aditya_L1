from typing import Dict, Any, List

class DecisionEngine:
    """Generates mission status and recommended actions backed by scientific justification."""
    
    def __init__(self):
        pass
        
    def generate_recommendation(self, forecast: Dict[str, Any]) -> Dict[str, Any]:
        state = forecast.get("state", "QUIET")
        
        status = "NOMINAL"
        actions = []
        mode = "NORMAL"
        cadence = "LOW"
        notes = ""
        justification = ""
        
        if state == "QUIET":
            actions.append("Maintain nominal operations.")
            justification = "Probability of M-class or higher is below threshold. Flux is stable."
        elif state == "WATCH":
            actions.append("Increase operator awareness.")
            actions.append("Review recent active region heating indices.")
            justification = "Elevated M-class probability detected."
        elif state == "WARNING":
            status = "ELEVATED"
            mode = "HIGH_CADENCE"
            cadence = "HIGH"
            actions.append("Switch SUIT to high cadence mode.")
            actions.append("Prepare for potential telemetry interruptions.")
            justification = "Significant probability of X-class event or rapidly rising flux."
        elif state == "ALERT":
            status = "CRITICAL"
            mode = "SAFE_MODE_STANDBY"
            cadence = "HIGH"
            actions.append("Prepare instruments for safe mode.")
            actions.append("Alert mission director.")
            justification = "High probability of X-class event with associated SEP risk. Current flux approaching threshold."
            
        return {
            "mission_status": status,
            "recommended_actions": actions,
            "observation_mode": mode,
            "cadence_recommendation": cadence,
            "operator_notes": notes,
            "scientific_justification": justification
        }

decision_engine = DecisionEngine()
