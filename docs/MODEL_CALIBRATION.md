# Model Calibration

ISRO requires calibrated probabilities for decision triggers, not raw unscaled scores.

## Calibration Methods

1. **Platt Scaling**: Fits parameters $A$ and $B$ to scale raw classifier logits:
   $$P(y=1|x) = \frac{1}{1 + \exp(A \cdot f(x) + B)}$$
2. **Temperature Scaling**: Scales multi-class logits with a single temperature parameter $T > 0$:
   $$P(y=c|x) = \frac{\exp(z_c / T)}{\sum_k \exp(z_k / T)}$$
3. **Isotonic Regression**: Fits a non-decreasing step function to map probabilities.
4. **Conformal Prediction**: Generates valid confidence intervals guaranteeing a target error rate (e.g. $1 - \alpha$).
