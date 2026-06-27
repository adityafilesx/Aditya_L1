# Experiment Registry

The Experiment Registry logs all training experiments and hyperparameter optimization sweeps, ensuring reproducible results.

## Experiment Logging Schema

- **`experiment_id`**: Unique ID mapping to a specific sweep or training trial.
- **`dataset_version`**: Dataset reference code.
- **`feature_version`**: Associated feature store configuration.
- **`target`**: Prediction target (e.g. `goes_class_next_1h`).
- **`algorithm`**: Specific model class.
- **`hyperparameters`**: Parameter key-value maps.
- **`training_time`**: Computational duration in seconds.
- **`validation_metrics`**: Complete evaluation metrics (Accuracy, F1, Loss, Brier).
- **`random_seed`**: Base seed for initialization.
- **`cross_validation_strategy`**: Used split method.
