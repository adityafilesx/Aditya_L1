import numpy as np
import pickle
from typing import Dict, Any, List
from backend.ml.models.base import BaseScientificModel

class HybridEnsembleModel(BaseScientificModel):
    def __init__(self, member_models: List[BaseScientificModel] = None, weights: List[float] = None, output_dim: int = 5, is_classifier: bool = True):
        self.member_models = member_models or []
        self.weights = weights or []
        self.output_dim = output_dim
        self.is_classifier = is_classifier
        self.variance = 0.0
        self.consensus_confidence = 1.0

    def train(self, X: np.ndarray, y: np.ndarray, **kwargs) -> Dict[str, Any]:
        if not self.member_models:
            raise ValueError("No member models provided for ensemble.")
        
        # Train all member models
        member_reports = []
        for i, model in enumerate(self.member_models):
            # Give slightly different splits or bootstrap samples
            indices = np.random.choice(len(X), len(X), replace=True)
            report = model.train(X[indices], y[indices])
            member_reports.append(report)
            
        # Determine weights based on validation performance or set equal weights
        if not self.weights:
            self.weights = [1.0 / len(self.member_models)] * len(self.member_models)
        else:
            # Normalize weights
            w_sum = sum(self.weights)
            self.weights = [w / w_sum for w in self.weights]
            
        return {"members_count": len(self.member_models), "weights": self.weights}

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.is_classifier:
            probas = self.predict_proba(X)
            return np.argmax(probas, axis=1) if self.output_dim > 1 else (probas[:, 1] > 0.5).astype(int)
        else:
            preds = np.zeros(X.shape[0])
            for w, model in zip(self.weights, self.member_models):
                preds += w * model.predict(X)
            return preds

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_classifier:
            raise ValueError("predict_proba is only available for classification.")
        
        n_samples = X.shape[0]
        accum_probs = np.zeros((n_samples, self.output_dim))
        
        # Collect member predictions
        member_preds = []
        for w, model in zip(self.weights, self.member_models):
            p = model.predict_proba(X)
            accum_probs += w * p
            member_preds.append(p)
            
        # Calculate ensemble variance across members
        # Shape: (members, samples, classes)
        member_preds_arr = np.array(member_preds)
        self.variance = float(np.mean(np.var(member_preds_arr, axis=0)))
        
        # consensus confidence is inverse of variance (normalized)
        self.consensus_confidence = float(np.clip(1.0 - 2.0 * self.variance, 0.0, 1.0))
        
        return accum_probs

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def load(self, path: str) -> None:
        with open(path, "rb") as f:
            loaded = pickle.load(f)
            self.__dict__.update(loaded.__dict__)

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        preds = self.predict(X)
        if self.is_classifier:
            probas = self.predict_proba(X)
            correct = np.sum(preds == y)
            acc = float(correct / len(y))
            eps = 1e-15
            probas = np.clip(probas, eps, 1.0 - eps)
            if self.output_dim > 1:
                y_one_hot = np.zeros((len(y), self.output_dim))
                y_one_hot[np.arange(len(y)), y.astype(int)] = 1.0
                loss = -np.mean(np.sum(y_one_hot * np.log(probas), axis=1))
            else:
                loss = -np.mean(y * np.log(probas[:, 1]) + (1.0 - y) * np.log(probas[:, 0]))
            return {
                "accuracy": acc,
                "loss": loss,
                "variance": self.variance,
                "consensus_confidence": self.consensus_confidence
            }
        else:
            mse = float(np.mean((preds - y) ** 2))
            mae = float(np.mean(np.abs(preds - y)))
            return {"mse": mse, "mae": mae, "variance": self.variance}
