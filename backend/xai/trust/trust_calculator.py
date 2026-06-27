from typing import Dict, Any, List
import time

class TrustEngine:
    """Generates and tracks Trust Score, Explanation Confidence, and Trust History over time."""
    
    def __init__(self):
        self.trust_history = []
        
    def calculate_trust(self, obs_quality: float, physics_score: float, model_reliability: float, event_similarity: float) -> Dict[str, Any]:
        # Trust score is calculated independently from forecast confidence
        trust_score = (obs_quality * 0.4) + (physics_score * 0.3) + (model_reliability * 0.2) + (event_similarity * 0.1)
        
        explanation_confidence = (obs_quality * 0.5) + (physics_score * 0.5)
        
        result = {
            "trust_score": trust_score,
            "explanation_confidence": explanation_confidence,
            "historical_reliability_index": event_similarity,
            "components": {
                "observation_quality": obs_quality,
                "physics_consistency": physics_score,
                "model_historical_accuracy": model_reliability
            },
            "timestamp": time.time()
        }
        
        self.trust_history.append(result)
        return result
        
    def get_history(self) -> List[Dict[str, Any]]:
        return self.trust_history

trust_engine = TrustEngine()
