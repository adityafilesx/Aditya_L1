from typing import Dict, Any
from backend.forecasting.engine.context import context_engine
from backend.forecasting.engine.state_machine import state_machine
from datetime import datetime
import uuid

class ForecastOrchestrator:
    """Coordinates Profile Selection, Inference, Calibration, Decision, and Storage."""
    
    def __init__(self):
        pass
        
    def run_pipeline(self, features: Dict[str, Any], horizon: str) -> Dict[str, Any]:
        """Runs the complete forecast generation pipeline."""
        forecast_id = str(uuid.uuid4())
        
        # 1. Build Context
        context = context_engine.build_context(features)
        
        # 2. Trigger Inference (mocked here, will be implemented in inference module)
        probabilities = {"A": 0.5, "B": 0.3, "C": 0.15, "M": 0.04, "X": 0.01}
        
        # 3. Update State Machine
        current_flux = features.get("current_flux", 1e-6)
        state = state_machine.evaluate_state(probabilities["M"], probabilities["X"], current_flux)
        
        # 4. Generate Forecast Object
        forecast = {
            "forecast_id": forecast_id,
            "timestamp": datetime.utcnow().isoformat(),
            "horizon": horizon,
            "probabilities": probabilities,
            "context": context,
            "state": state.value
        }
        
        return forecast

forecast_orchestrator = ForecastOrchestrator()
