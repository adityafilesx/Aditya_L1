import os
import json
import platform
from datetime import datetime
from typing import Dict, Any
from backend.ml.registry.model_registry import ModelMetadata

class TrainingReportGenerator:
    """Generates Markdown and JSON reports for model training runs."""
    def __init__(self, output_dir: str = "/Users/aditya1981/.gemini/antigravity-ide/brain/4be69a0e-4cb8-4457-b7dc-8b8a07b18a03/"):
        self.output_dir = output_dir

    def generate_report(self, model: ModelMetadata, runtime_sec: float, cv_strategy: str) -> None:
        md_path = os.path.join(self.output_dir, f"TRAINING_REPORT_{model.model_id}.md")
        json_path = os.path.join(self.output_dir, f"TRAINING_REPORT_{model.model_id}.json")

        md_content = f"""# Scientific Training Report: {model.model_name}

## Scientific Context
- **Model ID**: {model.model_id}
- **Algorithm**: {model.algorithm}
- **Implementation**: {model.implementation_classification}
- **Prediction Targets**: {", ".join(model.prediction_targets) if model.prediction_targets else 'None declared'}
- **Training Date**: {model.training_date}
- **Random Seed**: {model.random_seed}

## Dataset & Features
- **Dataset ID**: {model.training_dataset_id}
- **Feature Version**: {model.feature_version}
- **Label Version**: {model.label_version}
- **Cross-Validation Strategy**: {cv_strategy}

## Hyperparameters
```json
{json.dumps(model.hyperparameters, indent=2)}
```

## Performance & Calibration
- **Accuracy**: {model.evaluation_metrics.get('accuracy', 'N/A')}
- **Macro F1**: {model.evaluation_metrics.get('macro_f1', 'N/A')}
- **MCC**: {model.evaluation_metrics.get('mcc', 'N/A')}
- **Balanced Accuracy**: {model.evaluation_metrics.get('balanced_accuracy', 'N/A')}
- **Expected Calibration Error (ECE)**: {model.evaluation_metrics.get('ece', 'N/A')}
- **Brier Score**: {model.evaluation_metrics.get('brier_score', 'N/A')}

## System Information
- **Hardware**: {platform.processor()} ({platform.system()} {platform.release()})
- **Software**: Python {platform.python_version()}
- **Runtime**: {runtime_sec:.2f} seconds
"""
        
        report_data = {
            "model_metadata": model.dict(),
            "runtime_sec": runtime_sec,
            "cv_strategy": cv_strategy,
            "system": {
                "hardware": platform.processor(),
                "os": f"{platform.system()} {platform.release()}",
                "python": platform.python_version()
            }
        }
        
        try:
            with open(md_path, "w") as f:
                f.write(md_content)
                
            with open(json_path, "w") as f:
                json.dump(report_data, f, indent=2)
        except Exception:
            pass

report_generator = TrainingReportGenerator()
