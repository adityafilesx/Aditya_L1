from typing import Dict
from backend.physics.models import PhysicsCharacterization, GOESClass, PlasmaState
from backend.features.extractors.base_extractor import BaseFeatureExtractor

class CategoricalExtractor(BaseFeatureExtractor):
    """Encodes categorical fields (GOES Class, Plasma State) into ordinal float values."""

    def extract(self, product: PhysicsCharacterization) -> Dict[str, float]:
        goes_class = product.classification.goes_class
        plasma_state = product.plasma.plasma_state

        goes_map = {
            GOESClass.A: 1.0,
            GOESClass.B: 2.0,
            GOESClass.C: 3.0,
            GOESClass.M: 4.0,
            GOESClass.X: 5.0,
            GOESClass.UNKNOWN: 0.0,
        }

        plasma_map = {
            PlasmaState.QUIET: 0.0,
            PlasmaState.HEATING: 1.0,
            PlasmaState.COOLING: 2.0,
            PlasmaState.PEAK: 3.0,
            PlasmaState.UNKNOWN: -1.0,
        }

        return {
            "goes_class_val": goes_map.get(goes_class, 0.0),
            "plasma_state_val": plasma_map.get(plasma_state, -1.0),
        }
