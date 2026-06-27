import numpy as np
from typing import Dict, Any, Tuple

class CalibrationEngine:
    """Probability Calibration and Interval Generation Engine."""
    
    @staticmethod
    def expected_calibration_error(probs: np.ndarray, labels: np.ndarray, n_bins: int = 10) -> float:
        """Calculate Expected Calibration Error (ECE)."""
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        ece = 0.0
        n_samples = len(probs)
        
        for i in range(n_bins):
            bin_lower = bin_boundaries[i]
            bin_upper = bin_boundaries[i + 1]
            
            # Find samples in this bin
            in_bin = (probs >= bin_lower) & (probs < bin_upper)
            prop_in_bin = np.mean(in_bin)
            
            if prop_in_bin > 0:
                accuracy_in_bin = np.mean(labels[in_bin])
                avg_confidence_in_bin = np.mean(probs[in_bin])
                ece += prop_in_bin * np.abs(avg_confidence_in_bin - accuracy_in_bin)
                
        return float(ece)

    @staticmethod
    def platt_scaling_fit(logits: np.ndarray, labels: np.ndarray) -> Tuple[float, float]:
        """Fit Platt Scaling: returns sigmoid parameters A and B."""
        # Solves logistic regression on logits: p = 1 / (1 + exp(A * logits + B))
        # Simple gradient descent to find A, B
        A, B = -1.0, 0.0
        lr = 0.1
        epochs = 100
        
        # Clip labels to avoid log(0)
        y = np.clip(labels, 1e-6, 1.0 - 1e-6)
        
        for _ in range(epochs):
            pred = 1.0 / (1.0 + np.exp(np.clip(A * logits + B, -50.0, 50.0)))
            diff = pred - y
            
            dA = np.mean(diff * logits)
            dB = np.mean(diff)
            
            A -= lr * dA
            B -= lr * dB
            
        return float(A), float(B)

    @staticmethod
    def platt_scaling_predict(logits: np.ndarray, A: float, B: float) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(np.clip(A * logits + B, -50.0, 50.0)))

    @staticmethod
    def temperature_scaling_fit(logits: np.ndarray, labels: np.ndarray) -> float:
        """Fit Temperature Scaling: returns optimal temperature T > 0."""
        # logits of shape (N, C), labels of shape (N)
        # Minimize Cross Entropy Loss w.r.t Temperature T
        T = 1.0
        lr = 0.05
        epochs = 80
        
        if len(logits.shape) == 1:
            logits = logits.reshape(-1, 1)
            
        n_classes = logits.shape[1]
        if n_classes == 1:
            # Binary target
            y = labels.astype(float)
            for _ in range(epochs):
                p = 1.0 / (1.0 + np.exp(-logits.squeeze() / T))
                diff = p - y
                dT = -np.mean(diff * logits.squeeze() * (p * (1.0 - p)) / (T ** 2))
                T = max(0.1, T - lr * dT)
        else:
            # Multi-class target
            y_one_hot = np.zeros((len(labels), n_classes))
            y_one_hot[np.arange(len(labels)), labels.astype(int)] = 1.0
            
            for _ in range(epochs):
                scaled_logits = logits / T
                shift_logits = scaled_logits - np.max(scaled_logits, axis=1, keepdims=True)
                probs = np.exp(shift_logits) / np.sum(np.exp(shift_logits), axis=1, keepdims=True)
                
                # Cross entropy derivative w.r.t T
                # dL/dT = sum_{i,c} (p_{ic} - y_{ic}) * z_{ic} * (-1/T^2)
                diff = probs - y_one_hot
                dT = np.mean(np.sum(diff * logits, axis=1)) / (T ** 2)
                T = max(0.1, T - lr * dT)
                
        return float(T)

    @staticmethod
    def isotonic_regression_fit(probs: np.ndarray, labels: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Fit Isotonic Regression (simplified pool adjacent violators algorithm)."""
        idx = np.argsort(probs)
        sorted_probs = probs[idx]
        sorted_labels = labels[idx].astype(float)
        
        # Basic binning/averaging to enforce monotonicity
        n = len(probs)
        values = sorted_labels.copy()
        
        # Iterate and average adjacent violators
        for _ in range(10):
            violators_found = False
            i = 0
            while i < n - 1:
                if values[i] > values[i + 1]:
                    # Violator found
                    avg = (values[i] + values[i + 1]) / 2.0
                    values[i] = avg
                    values[i + 1] = avg
                    violators_found = True
                i += 1
            if not violators_found:
                break
                
        return sorted_probs, values

    @staticmethod
    def isotonic_regression_predict(probs: np.ndarray, sorted_probs: np.ndarray, values: np.ndarray) -> np.ndarray:
        return np.interp(probs, sorted_probs, values)

    @staticmethod
    def conformal_prediction_intervals(scores: np.ndarray, labels: np.ndarray, alpha: float = 0.1) -> Tuple[float, np.ndarray, np.ndarray]:
        """Compute Conformal Prediction intervals (guaranteeing 1 - alpha coverage)."""
        # residuals for regression or 1 - proba for classification
        residuals = np.abs(scores - labels)
        q = np.percentile(residuals, 100.0 * (1.0 - alpha))
        
        lower_bounds = scores - q
        upper_bounds = scores + q
        return float(q), lower_bounds, upper_bounds
