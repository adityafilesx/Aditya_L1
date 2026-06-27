import numpy as np
import pickle
from typing import Dict, Any
from backend.ml.models.base import BaseScientificModel
from backend.ml.models.utils import DecisionStump, softmax

class RandomForestModel(BaseScientificModel):
    def __init__(self, n_estimators: int = 10, output_dim: int = 5, is_classifier: bool = True):
        self.n_estimators = n_estimators
        self.output_dim = output_dim
        self.is_classifier = is_classifier
        self.estimators = []

    def train(self, X: np.ndarray, y: np.ndarray, **kwargs) -> Dict[str, Any]:
        self.estimators = []
        n_samples = len(X)
        
        for _ in range(self.n_estimators):
            # Bootstrap sample
            indices = np.random.choice(n_samples, n_samples, replace=True)
            X_b, y_b = X[indices], y[indices]
            
            if self.is_classifier and self.output_dim > 1:
                # Store class-wise decision stumps
                stumps = []
                for c in range(self.output_dim):
                    stump = DecisionStump()
                    # Binary targets for class c
                    y_binary = (y_b == c).astype(float) * 2.0 - 1.0
                    stump.fit(X_b, y_binary)
                    stumps.append(stump)
                self.estimators.append(stumps)
            else:
                stump = DecisionStump()
                stump.fit(X_b, y_b)
                self.estimators.append(stump)
                
        return {"n_estimators": len(self.estimators), "n_samples": n_samples}

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.estimators:
            raise ValueError("Model is not trained yet.")
        if self.is_classifier:
            probas = self.predict_proba(X)
            return np.argmax(probas, axis=1) if self.output_dim > 1 else (probas[:, 1] > 0.5).astype(int)
        
        # Regression average prediction
        preds = np.zeros(X.shape[0])
        for stump in self.estimators:
            preds += stump.predict(X)
        return preds / len(self.estimators)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.estimators:
            raise ValueError("Model is not trained yet.")
        if not self.is_classifier:
            raise ValueError("predict_proba is only available for classification.")
        
        n_samples = X.shape[0]
        if self.output_dim > 1:
            votes = np.zeros((n_samples, self.output_dim))
            for stumps in self.estimators:
                for c in range(self.output_dim):
                    pred = stumps[c].predict(X)
                    votes[:, c] += (pred > 0).astype(float)
            # Add eps to avoid divide by zero
            return softmax(votes)
        else:
            votes = np.zeros(n_samples)
            for stump in self.estimators:
                pred = stump.predict(X)
                votes += (pred > 0).astype(float)
            probs = votes / len(self.estimators)
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
