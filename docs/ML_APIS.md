# Machine Learning REST APIs

Exposes HTTP endpoints for model administration and evaluations.

- **`GET /api/ml/models`**: List registered models.
- **`GET /api/ml/registry`**: Overview of active model.
- **`GET /api/ml/experiments`**: List experiment runs.
- **`GET /api/ml/datasets`**: List versioned training datasets.
- **`GET /api/ml/targets`**: List prediction target labels.
- **`GET /api/ml/evaluation`**: Get detailed accuracy, F1, PR/ROC curves, confusion matrix.
- **`GET /api/ml/calibration`**: Expected calibration error and scaling coefficients.
- **`GET /api/ml/metrics`**: Comparison summary matrix.
- **`GET /api/ml/monitoring`**: Real-time feature drift and system usage.
- **`POST /api/ml/train`**: Trigger training run with selected algorithm and CV split.
- **`POST /api/ml/models/{model_id}/stage`**: Promote model stage (ACTIVE, EXPERIMENTAL, ARCHIVED).
