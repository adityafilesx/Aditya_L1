from typing import Dict, Any, List
import time

class ProvenanceEngine:
    """Manages forecast provenance and logs operator overrides."""
    
    def __init__(self):
        self.overrides = []
        
    def build_lineage(self, obs_id: str, physics_ver: str, feat_ver: str, dataset_ver: str, model_id: str, rule_ver: str) -> Dict[str, str]:
        return {
            "observation_id": obs_id,
            "physics_engine_version": physics_ver,
            "feature_schema_version": feat_ver,
            "dataset_version": dataset_ver,
            "model_version_id": model_id,
            "scientific_rules_version": rule_ver
        }
        
    def record_override(self, forecast_id: str, operator_id: str, original_state: str, new_state: str, reason: str) -> Dict[str, Any]:
        override_log = {
            "forecast_id": forecast_id,
            "operator_id": operator_id,
            "original_state": original_state,
            "new_state": new_state,
            "reason": reason,
            "timestamp": time.time(),
            "eventual_outcome": "PENDING"
        }
        self.overrides.append(override_log)
        return override_log

provenance_engine = ProvenanceEngine()
