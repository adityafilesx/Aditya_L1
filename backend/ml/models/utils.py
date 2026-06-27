import numpy as np
from typing import Dict, Any, Tuple

def softmax(x: np.ndarray) -> np.ndarray:
    shift_x = x - np.max(x, axis=-1, keepdims=True)
    exps = np.exp(shift_x)
    return exps / np.sum(exps, axis=-1, keepdims=True)

def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -50.0, 50.0)))

class PureNumpyMLP:
    """A simple 1-hidden-layer MLP in pure numpy supporting classification and regression."""
    def __init__(self, input_dim: int, hidden_dim: int = 16, output_dim: int = 1, is_classifier: bool = True):
        self.is_classifier = is_classifier
        self.output_dim = output_dim
        
        # Initialize weights
        self.W1 = np.random.randn(input_dim, hidden_dim) * np.sqrt(2.0 / input_dim)
        self.b1 = np.zeros((1, hidden_dim))
        self.W2 = np.random.randn(hidden_dim, output_dim) * np.sqrt(2.0 / hidden_dim)
        self.b2 = np.zeros((1, output_dim))

    def forward(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        # Linear + Relu
        z1 = np.dot(X, self.W1) + self.b1
        a1 = np.maximum(0, z1) # ReLU
        # Output
        z2 = np.dot(a1, self.W2) + self.b2
        if self.is_classifier:
            if self.output_dim == 1:
                out = sigmoid(z2)
            else:
                out = softmax(z2)
        else:
            out = z2
        return out, a1

    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int = 100, lr: float = 0.01) -> float:
        # y should be shape (N, output_dim)
        if self.is_classifier and self.output_dim > 1 and len(y.shape) == 1:
            # One-hot encode y
            num_classes = self.output_dim
            y_one_hot = np.zeros((len(y), num_classes))
            y_one_hot[np.arange(len(y)), y.astype(int)] = 1.0
            y = y_one_hot
        elif len(y.shape) == 1:
            y = y.reshape(-1, 1)

        loss_history = 0.0
        for _ in range(epochs):
            # Forward pass
            out, a1 = self.forward(X)
            # Loss and gradient
            diff = out - y
            loss_history = np.mean(diff ** 2)
            
            # Backpropagation
            dW2 = np.dot(a1.T, diff) / len(X)
            db2 = np.mean(diff, axis=0, keepdims=True)
            
            da1 = np.dot(diff, self.W2.T)
            dz1 = da1 * (a1 > 0) # ReLU derivative
            
            dW1 = np.dot(X.T, dz1) / len(X)
            db1 = np.mean(dz1, axis=0, keepdims=True)
            
            # Update weights
            self.W1 -= lr * dW1
            self.b1 -= lr * db1
            self.W2 -= lr * dW2
            self.b2 -= lr * db2
            
        return float(loss_history)


class DecisionStump:
    def __init__(self):
        self.polarity = 1
        self.feature_idx = None
        self.threshold = None
        self.alpha = None
        self.left_val = 0.0
        self.right_val = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        n_samples, n_features = X.shape
        min_error = float('inf')
        
        # Simple search for a splitting threshold
        for feature_i in range(n_features):
            X_column = X[:, feature_i]
            thresholds = np.percentile(X_column, [25, 50, 75])
            for threshold in thresholds:
                for polarity in [1, -1]:
                    predictions = np.ones(n_samples)
                    if polarity == 1:
                        predictions[X_column < threshold] = -1
                    else:
                        predictions[X_column > threshold] = -1
                    
                    error = np.mean((y - predictions) ** 2)
                    if error < min_error:
                        min_error = error
                        self.polarity = polarity
                        self.feature_idx = feature_i
                        self.threshold = threshold
                        
        # Calculate values
        if self.feature_idx is not None:
            left_mask = X[:, self.feature_idx] < self.threshold
            if self.polarity == -1:
                left_mask = ~left_mask
            self.left_val = np.mean(y[left_mask]) if np.any(left_mask) else 0.0
            self.right_val = np.mean(y[~left_mask]) if np.any(~left_mask) else 0.0

    def predict(self, X: np.ndarray) -> np.ndarray:
        n_samples = X.shape[0]
        if self.feature_idx is None:
            return np.zeros(n_samples)
        
        X_column = X[:, self.feature_idx]
        predictions = np.zeros(n_samples)
        left_mask = X_column < self.threshold
        if self.polarity == -1:
            left_mask = ~left_mask
            
        predictions[left_mask] = self.left_val
        predictions[~left_mask] = self.right_val
        return predictions


class PureNumpyBoosting:
    """A gradient boosting stump ensemble."""
    def __init__(self, n_estimators: int = 10, learning_rate: float = 0.1, output_dim: int = 1, is_classifier: bool = True):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.output_dim = output_dim
        self.is_classifier = is_classifier
        self.estimators = []

    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int = 10) -> float:
        # Initialize output
        n_samples = len(X)
        if self.is_classifier and self.output_dim > 1:
            # One-hot y
            if len(y.shape) == 1:
                y_one_hot = np.zeros((n_samples, self.output_dim))
                y_one_hot[np.arange(n_samples), y.astype(int)] = 1.0
                y = y_one_hot
            F = np.zeros((n_samples, self.output_dim))
        else:
            if len(y.shape) == 1:
                y = y.reshape(-1, 1)
            F = np.zeros((n_samples, 1))

        self.estimators = []
        for _ in range(self.n_estimators):
            if self.is_classifier and self.output_dim > 1:
                probs = softmax(F)
                residuals = y - probs
                stumps_for_classes = []
                for c in range(self.output_dim):
                    stump = DecisionStump()
                    stump.fit(X, residuals[:, c])
                    F[:, c] += self.learning_rate * stump.predict(X)
                    stumps_for_classes.append(stump)
                self.estimators.append(stumps_for_classes)
            else:
                residuals = y - F
                stump = DecisionStump()
                stump.fit(X, residuals[:, 0])
                F[:, 0] += self.learning_rate * stump.predict(X)
                self.estimators.append(stump)
        
        final_loss = np.mean((y - (softmax(F) if self.is_classifier and self.output_dim > 1 else F)) ** 2)
        return float(final_loss)

    def predict_raw(self, X: np.ndarray) -> np.ndarray:
        n_samples = len(X)
        if self.is_classifier and self.output_dim > 1:
            F = np.zeros((n_samples, self.output_dim))
            for stumps in self.estimators:
                for c in range(self.output_dim):
                    F[:, c] += self.learning_rate * stumps[c].predict(X)
            return F
        else:
            F = np.zeros((n_samples, 1))
            for stump in self.estimators:
                F[:, 0] += self.learning_rate * stump.predict(X)
            return F
