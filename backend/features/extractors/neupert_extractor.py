from typing import Dict
from backend.physics.models import PhysicsCharacterization
from backend.features.extractors.base_extractor import BaseFeatureExtractor

class NeupertExtractor(BaseFeatureExtractor):
    """Extracts Neupert effect parameters."""

    def extract(self, product: PhysicsCharacterization) -> Dict[str, float]:
        ne = product.neupert
        return {
            "neupert_offset": float(ne.neupert_offset) if ne.neupert_offset is not None else 0.0,
            "neupert_score": float(ne.neupert_score) if ne.neupert_score is not None else 0.0,
            "neupert_consistency": float(ne.neupert_consistency) if ne.neupert_consistency is not None else 0.0,
            "neupert_confidence": float(ne.neupert_confidence) if ne.neupert_confidence is not None else 0.0,
        }
