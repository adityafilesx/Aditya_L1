# Model Registry

The Model Registry provides version control, audit trails, and deployment stage tracking for all trained solar forecasting models.

## Immutable Records

Every registered model is immutable. Any new training run or configuration modification generates a new unique `Model ID`.

## Model Metadata Schema

| Field | Description |
| --- | --- |
| `model_id` | Unique identifier (`model-[algo]-[timestamp]`) |
| `model_name` | Human-readable name |
| `architecture` | Model architecture keyword |
| `algorithm` | Specific training algorithm |
| `version` | Semantic version string |
| `training_dataset_id` | Unique ID of dataset used in training |
| `feature_version` | Feature store schema version |
| `label_version` | Target label version |
| `training_date` | Date/time stamp of training completion |
| `hyperparameters` | Dictionary of key training parameters |
| `evaluation_metrics` | Validation performance scores |
| `calibration_version` | Probability calibration run identifier |
| `serving_status` | Current readiness state (`READY` / `OFFLINE`) |
| `deployment_stage` | Current stage (`ACTIVE`, `EXPERIMENTAL`, `ARCHIVED`) |

## Lifecycle Stages

- **ACTIVE**: The primary model selected for nowcasting and forecasting evaluations.
- **EXPERIMENTAL**: Models under test or validation tracking.
- **ARCHIVED**: Deprecated or legacy models.
