from typing import Dict, Any, List
import time

class MissionPlaybackEngine:
    """Simulates active mission playback and automated scenario scripts (Demo Mode)."""
    
    def __init__(self):
        self.playback_speed = 1.0 # 1x, 5x, 10x, 100x
        self.is_playing = False
        
    def trigger_demo_mode(self) -> Dict[str, Any]:
        """Automatically walks through a mock solar flare scenario from ingestion to action."""
        return {
            "scenario": "X-CLASS_FLARE_TRIGGER",
            "steps": [
                {"timestamp": time.time(), "layer": "Observation", "status": "Telemetry spike detected", "flux": 1.2e-4},
                {"timestamp": time.time() + 1, "layer": "Physics", "status": "Heating index elevated to 2.8", "heating_index": 2.8},
                {"timestamp": time.time() + 2, "layer": "ML Inference", "status": "P(X-Class) evaluated at 72%", "p_x_class": 0.72},
                {"timestamp": time.time() + 3, "layer": "Decision Intelligence", "status": "Alert elevated to RED. Recommended safe mode.", "mode": "SAFE_MODE"}
            ]
        }

mission_playback_engine = MissionPlaybackEngine()
