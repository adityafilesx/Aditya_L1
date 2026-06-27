import os
import json
from backend.ml.datasets.dataset_registry import DatasetRecord

class DatasetSummaryGenerator:
    """Generates Markdown and JSON reports for scientific dataset provenance."""
    def __init__(self, output_dir: str = "/Users/aditya1981/.gemini/antigravity-ide/brain/4be69a0e-4cb8-4457-b7dc-8b8a07b18a03/"):
        self.output_dir = output_dir

    def generate_summary(self, dataset: DatasetRecord) -> None:
        md_path = os.path.join(self.output_dir, f"DATASET_SUMMARY_{dataset.dataset_id}.md")
        json_path = os.path.join(self.output_dir, f"DATASET_METADATA_{dataset.dataset_id}.json")

        md_content = f"""# Dataset Summary: {dataset.dataset_id}

## Scientific Provenance
- **Dataset Version**: {dataset.dataset_version}
- **Feature Registry Version**: {dataset.feature_registry_version}
- **Feature Engineering Version**: {dataset.feature_engineering_version}
- **Physics Engine Version**: {dataset.physics_engine_version}
- **Source Observation Version**: {dataset.source_observation_version}
- **Label Version**: {dataset.label_version}
- **Creation Timestamp**: {dataset.creation_time}
- **Checksum**: {dataset.checksum}

## Dataset Statistics
- **Total Samples**: {dataset.num_samples}
- **Feature Count**: {dataset.feature_count}
- **Positive Labels**: {dataset.positive_labels}
- **Negative Labels**: {dataset.negative_labels}
- **Missing Values**: {dataset.missing_values}
- **Forecast Horizon**: {dataset.forecast_horizon}
- **Temporal Window**: {dataset.time_window}

## Splits
- **Training**: {dataset.training_split * 100}%
- **Validation**: {dataset.validation_split * 100}%
- **Testing**: {dataset.testing_split * 100}%

## Class Distribution
```json
{json.dumps(dataset.class_distribution, indent=2)}
```
"""
        try:
            with open(md_path, "w") as f:
                f.write(md_content)
                
            with open(json_path, "w") as f:
                json.dump(dataset.dict(), f, indent=2)
        except Exception:
            pass

summary_generator = DatasetSummaryGenerator()
