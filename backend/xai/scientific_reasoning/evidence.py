from typing import Dict, Any, List

class EvidenceItem:
    def __init__(self, category: str, name: str, weight: float, direction: str, confidence: float, source: str):
        self.category = category
        self.name = name
        self.weight = weight
        self.direction = direction # "supports" or "opposes"
        self.confidence = confidence
        self.source = source
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "name": self.name,
            "weight": self.weight,
            "direction": self.direction,
            "confidence": self.confidence,
            "source": self.source
        }

class ScientificEvidenceEngine:
    """Compiles and ranks multi-faceted flare evidence."""
    
    def __init__(self):
        pass
        
    def compile_evidence(self, features: Dict[str, Any], predictions: Dict[str, Any]) -> List[Dict[str, Any]]:
        evidence = []
        
        # 1. Observation Evidence
        obs_qual = features.get("overall_quality", 0.95)
        evidence.append(EvidenceItem("Observation", "Telemetry Integrity", 0.8, "supports", obs_qual, "GOES-15/XSM Receiver"))
        
        # 2. Physics Evidence
        heating = features.get("heating_index", 0.0)
        if heating > 2.0:
            evidence.append(EvidenceItem("Physics", "Thermal Heating Ascent", 0.95, "supports", 0.9, "SUIT Solar Filter"))
        else:
            evidence.append(EvidenceItem("Physics", "Thermal Heating Inactive", 0.5, "opposes", 0.8, "SUIT Solar Filter"))
            
        # 3. Temporal Evidence
        flux_deriv = features.get("flux_derivative", 0.0)
        if flux_deriv > 1e-6:
            evidence.append(EvidenceItem("Temporal", "Flux Acceleration Trigger", 0.9, "supports", 0.85, "Flux Gradient Extractor"))
            
        # 4. Model Evidence
        m_prob = predictions.get("M", 0.0)
        evidence.append(EvidenceItem("Model", "XGBoost Reference Confidence", 0.7, "supports" if m_prob > 0.3 else "opposes", 0.78, "ML Registry"))
        
        # Sort evidence by weight descending
        evidence.sort(key=lambda x: x.weight, reverse=True)
        return [e.to_dict() for e in evidence]

scientific_evidence_engine = ScientificEvidenceEngine()
