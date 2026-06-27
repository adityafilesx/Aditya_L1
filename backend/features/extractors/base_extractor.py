from abc import ABC, abstractmethod
from typing import Dict
from backend.physics.models import PhysicsCharacterization

class BaseFeatureExtractor(ABC):
    """Base interface for all feature extractors."""

    @abstractmethod
    def extract(self, product: PhysicsCharacterization) -> Dict[str, float]:
        """Extract features from the physics characterization product.

        Returns a dictionary mapping feature names to float values.
        """
        pass
