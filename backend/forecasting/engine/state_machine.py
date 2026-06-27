import os
import json
from enum import Enum
from typing import Dict, Any

class ForecastState(Enum):
    QUIET = "QUIET"
    WATCH = "WATCH"
    WARNING = "WARNING"
    ALERT = "ALERT"
    RECOVERY = "RECOVERY"

class ForecastStateMachine:
    """Manages the mission state transitions based on forecast probabilities and flux."""
    
    def __init__(self):
        self.current_state = ForecastState.QUIET
        self.history = []
        
    def evaluate_state(self, p_m_class: float, p_x_class: float, current_flux: float) -> ForecastState:
        # Simple state machine logic based on active event probabilities
        new_state = self.current_state
        
        if p_x_class > 0.5 or current_flux > 1e-4:
            new_state = ForecastState.ALERT
        elif p_m_class > 0.5 or p_x_class > 0.2 or current_flux > 1e-5:
            if self.current_state != ForecastState.ALERT: # don't downgrade immediately
                new_state = ForecastState.WARNING
        elif p_m_class > 0.2:
            if self.current_state not in [ForecastState.ALERT, ForecastState.WARNING]:
                new_state = ForecastState.WATCH
        else:
            if self.current_state in [ForecastState.ALERT, ForecastState.WARNING]:
                new_state = ForecastState.RECOVERY
            else:
                new_state = ForecastState.QUIET
                
        if new_state != self.current_state:
            self.history.append({
                "from": self.current_state.value,
                "to": new_state.value,
                "reason": f"Probabilities M={p_m_class:.2f}, X={p_x_class:.2f}, Flux={current_flux:.2e}"
            })
            self.current_state = new_state
            
        return self.current_state

state_machine = ForecastStateMachine()
