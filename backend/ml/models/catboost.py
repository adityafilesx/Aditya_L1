import numpy as np
import pickle
from typing import Dict, Any
from backend.ml.models.base import BaseScientificModel
from backend.ml.models.utils import PureNumpyBoosting, softmax

class CatBoostModel(BaseScientificModel):
    def __init__(self, n_estimators: int = 20, learning_rate: float = 0.05, output_dim: int = 5, is_classifier: bool = True):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.output_dim = output_dim
        self.is_classifier = is_classifier
        self.model = None

    def train(self, X: np.ndarray, y: np.ndarray, **kwargs) -> Dict[str, Any]:
        self.model = PureNumpyBoosting(
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate,
            output_dim=self.output_dim,
            is_classifier=self.is_classifier
        )
        final_loss = self.model.fit(X, y)
        return {"loss": final_loss, "n_samples": len(X), "features_count": X.shape[1]}

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model is not trained yet.")
        raw = self.model.predict_raw(X)
        if self.is_classifier:
            if self.output_dim > 1:
                return np.argmax(raw, axis=1)
            else:
                return (raw.squeeze() > 0.0).astype(int)
        return raw.squeeze()

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model is not trained yet.")
        if not self.is_classifier:
            raise ValueError("predict_proba is only available for classification.")
        raw = self.model.predict_raw(X)
        if self.output_dim > 1:
            return softmax(raw)
        else:
            probs = 1.0 / (1.0 + np.exp(-np.clip(raw, -50.0, 50.0)))
            return np.column_stack((1.0 - probs, probs))

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
            return {"accuracy": acc, "loss": loss}
        else:
            mse = float(np.mean((preds - y) ** 2))
            mae = float(np.mean(np.abs(preds - y)))
            return {"mse": mse, "mae": mae}
