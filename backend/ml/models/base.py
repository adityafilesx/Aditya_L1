from abc import ABC, abstractmethod
from typing import Dict, Any, Union
import numpy as np

class BaseScientificModel(ABC):
    """Abstract Base Class for all machine learning models in the platform."""

    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray, **kwargs) -> Dict[str, Any]:
        """Train the model on feature matrix X and target y."""
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generate point predictions."""
        pass

    @abstractmethod
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Generate prediction probabilities (calibrated or raw classifier outputs)."""
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """Serialize and save the model state to disk."""
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """Deserialize and load the model state from disk."""
        pass

    @abstractmethod
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """Compute evaluation metrics on validation/test set."""
        pass
