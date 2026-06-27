# Model Comparison Platform

The Model Comparison Platform enables operators to evaluate multiple architectures simultaneously.

## Features

- **Consensus Matrix**: Scores accuracy, validation F1, Brier, and expected calibration error across models.
- **Stage Progression**: Select the best model and promote it to `ACTIVE` serving status, replacing the previous active model.
- **WebSocket Feeds**: Pushes training updates and validation parameters live.
