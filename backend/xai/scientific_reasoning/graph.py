from typing import Dict, Any, List

class ReasoningGraphEngine:
    """Generates a causal reasoning graph from Observation -> Physics -> Feature -> Model -> Forecast -> Decision."""
    
    def __init__(self):
        pass
        
    def build_graph(self, features: Dict[str, Any], predictions: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
        nodes = [
            {"id": "OBS", "label": "Observation Layer", "description": "High-fidelity telemetry ingested.", "type": "observation"},
            {"id": "PHYS", "label": "Physics Engine", "description": f"Heating Index: {features.get('heating_index', 0.0):.2f}", "type": "physics"},
            {"id": "FEAT", "label": "Feature store", "description": "Feature vector extracted and normalized.", "type": "feature"},
            {"id": "MODEL", "label": "Model Registry", "description": f"Target predictions generated. P(M)={predictions.get('M', 0.0):.2f}", "type": "model"},
            {"id": "DECISION", "label": "Decision Support", "description": decision.get("observation_mode", "NOMINAL"), "type": "decision"}
        ]
        
        edges = [
            {"source": "OBS", "target": "PHYS", "relation": "drives_physics_characterization"},
            {"source": "PHYS", "target": "FEAT", "relation": "populates_features"},
            {"source": "FEAT", "target": "MODEL", "relation": "feeds_inference"},
            {"source": "MODEL", "target": "DECISION", "relation": "triggers_action"}
        ]
        
        return {
            "nodes": nodes,
            "edges": edges
        }

reasoning_graph_engine = ReasoningGraphEngine()
