import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    Module 4: Recommendation Engine
    Generates context-aware operational recommendations for mission controllers 
    based on current state, trajectory, confidence, and telemetry health.
    """
    def __init__(self):
        # Define hierarchy for trajectory analysis
        self.state_hierarchy = {
            "QUIET": 0, 
            "WATCH": 1, 
            "RECOVERY": 1.5, 
            "PRE-ALERT": 2, 
            "ALERT": 3, 
            "HIGH ALERT": 4
        }
        
    def generate_recommendations(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses the unified decision context and outputs actionable recommendations.
        """
        state = decision_context.get("operational_state", "QUIET")
        prev_state = decision_context.get("previous_state", "QUIET")
        health = decision_context.get("telemetry_health", "OK")
        is_confident = decision_context.get("is_confident", True)
        flux_class = decision_context.get("estimated_goes_class", "A")

        primary_action = "Nominal operations"
        secondary_actions = []
        criticality = "NOMINAL"
        
        # 1. Trajectory Analysis (Escalating vs De-escalating)
        escalating = self._is_escalating(prev_state, state)
        
        # 2. Base Rules for State
        if state == "HIGH ALERT":
            primary_action = "DEPLOY ATTENUATOR IMMEDIATELY"
            secondary_actions = [
                f"Verify payload safety for predicted {flux_class} flare.",
                "Halt non-essential commanding."
            ]
            criticality = "IMMEDIATE"
            
        elif state == "ALERT":
            primary_action = "Prepare Attenuator Deployment"
            secondary_actions = [
                f"Flare in progress ({flux_class} level).",
                "Review automated payload safety limits."
            ]
            criticality = "WITHIN 5 MIN"
            
        elif state == "PRE-ALERT":
            primary_action = "Increase Telemetry Downlink Rate"
            secondary_actions = [
                "Flare imminent. Monitor X-ray flux closely."
            ]
            criticality = "WITHIN 15 MIN"
            if escalating:
                secondary_actions.append("Rapid escalation detected. Standby for ALERT.")
                
        elif state == "WATCH":
            primary_action = "Elevated Monitoring"
            secondary_actions = ["Solar activity increasing above baseline."]
            criticality = "ROUTINE"
            
        elif state == "RECOVERY":
            primary_action = "Maintain Current Configuration"
            secondary_actions = ["Event cooling down.", "Do not retract attenuator until flux normalizes."]
            criticality = "ROUTINE"
            
        elif state == "QUIET":
            primary_action = "Nominal Operations"
            secondary_actions = ["No immediate threat."]
            criticality = "NOMINAL"
            
        # 3. Telemetry Health Context
        if health == "GAP":
            secondary_actions.append("WARNING: Telemetry gap detected. Recommendations may be based on stale data.")
        elif health == "ATTENUATOR_ON" and state in ["HIGH ALERT", "ALERT"]:
            primary_action = "Maintain Attenuator Deployment"
            secondary_actions.insert(0, "Attenuator already active. Ensure thermal stability.")
            criticality = "NOMINAL" # Already handled
            
        # 4. Confidence Context
        if not is_confident and state in ["HIGH ALERT", "ALERT", "PRE-ALERT"]:
            primary_action = "[MANUAL VERIFICATION REQUIRED] " + primary_action
            secondary_actions.insert(0, "CRITICAL: Model confidence is low. Verify with secondary instruments (e.g., SUIT) before commanding.")
            criticality = "IMMEDIATE"
            
        return {
            "primary_action": primary_action,
            "secondary_actions": secondary_actions,
            "time_criticality": criticality,
            "is_escalating": escalating
        }
        
    def _is_escalating(self, prev_state: str, current_state: str) -> bool:
        prev_val = self.state_hierarchy.get(prev_state, 0)
        curr_val = self.state_hierarchy.get(current_state, 0)
        return curr_val > prev_val
