from typing import Dict, Any
import random

class SystemHealthManager:
    """Tracks physical resources and reports real-time system metrics."""
    
    def __init__(self):
        self.failed_subsystems = set()
        
    def inject_failure(self, subsystem: str):
        self.failed_subsystems.add(subsystem)
        
    def clear_failures(self):
        self.failed_subsystems.clear()
        
    def get_system_health(self) -> Dict[str, Any]:
        if "cpu" in self.failed_subsystems:
            cpu_usage = 99.9
        else:
            cpu_usage = random.uniform(20.0, 50.0)
            
        return {
            "resources": {
                "cpu_usage_pct": cpu_usage,
                "memory_used_gb": 12.4,
                "memory_total_gb": 32.0,
                "disk_free_pct": 68.4
            },
            "services": {
                "telemetry_stream": "FAILED" if "telemetry" in self.failed_subsystems else "NOMINAL",
                "physics_engine": "FAILED" if "physics" in self.failed_subsystems else "NOMINAL",
                "inference_engine": "FAILED" if "inference" in self.failed_subsystems else "NOMINAL",
                "api_gateway": "NOMINAL"
            }
        }

system_health_manager = SystemHealthManager()
