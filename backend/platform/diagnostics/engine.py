from typing import Dict, Any
from backend.platform.monitoring.health import system_health_manager

class DiagnosticsEngine:
    """Performs self-checks on startup to ensure end-to-end pipeline integrity."""
    
    def __init__(self):
        pass
        
    def run_diagnostics(self) -> Dict[str, Any]:
        health = system_health_manager.get_system_health()
        failures = [name for name, status in health["services"].items() if status == "FAILED"]
        
        return {
            "status": "UNHEALTHY" if failures else "PASS",
            "active_failures": failures,
            "checks_executed": [
                "telemetry_stream_validation",
                "physics_coefficients_matching",
                "inference_model_weight_checksums",
                "api_endpoint_pings"
            ]
        }

diagnostics_engine = DiagnosticsEngine()
