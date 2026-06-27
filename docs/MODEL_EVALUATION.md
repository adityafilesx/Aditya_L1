# Model Evaluation

The Evaluation Engine computes mathematical metrics to assess predictive performance on out-of-sample data.

## Classification Metrics

- **Accuracy**: Fraction of correct predictions.
- **Precision**: Macro-averaged class precision.
- **Recall**: Macro-averaged class recall.
- **F1 Score**: Harmonic mean of Precision and Recall.
- **Matthews Correlation Coefficient (MCC)**: High-quality metric for unbalanced multiclass problems.
- **Brier Score**: Evaluates accuracy of probabilistic predictions.
- **Expected Calibration Error (ECE)**: Difference between confidence and accuracy.

## Visualizations Supported

- **Confusion Matrix**: Tabulates actual vs predicted class breakdowns.
- **Reliability Diagram**: Displays predicted probabilities vs actual class frequencies in equal-width bins.
- **Learning Curves**: Chart of training vs validation scores over subset sizes to detect overfitting or data gaps.
