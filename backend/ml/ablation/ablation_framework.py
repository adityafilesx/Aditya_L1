import os
import json
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from backend.ml.registry.model_registry import ModelMetadata

class AblationExperiment(BaseModel):
    experiment_id: str
    target_prediction: str
    baseline_model_id: str
    feature_groups_disabled: List[str]
    evaluation_metrics: Dict[str, Any]
    delta_mcc: float
    delta_f1: float
    delta_accuracy: float
    timestamp: str

class AblationFramework:
    """Manages ablation studies by tracking performance drop when feature groups are removed."""
    FEATURE_GROUPS = [
        "Observation Features",
        "Physics Features",
        "Thermal Features",
        "Temporal Features",
        "Spectral Features",
        "Plasma Features",
        "Derived Indices",
        "Quality Metrics"
    ]
    
    def __init__(self, storage_path: str = "data/ml_ablation_studies.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.experiments: List[AblationExperiment] = []
        self._load_experiments()

    def _load_experiments(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    self.experiments = [AblationExperiment(**exp) for exp in data]
            except Exception:
                self.experiments = []

    def _save_experiments(self) -> None:
        with open(self.storage_path, "w") as f:
            json.dump([exp.dict() for exp in self.experiments], f, indent=2)

    def register_experiment(self, experiment: AblationExperiment) -> None:
        self.experiments.append(experiment)
        self._save_experiments()
        
    def generate_ablation_report(self, target_prediction: str, output_dir: str = "/Users/aditya1981/.gemini/antigravity-ide/brain/4be69a0e-4cb8-4457-b7dc-8b8a07b18a03/") -> None:
        relevant_exps = [e for e in self.experiments if e.target_prediction == target_prediction]
        if not relevant_exps:
            return
            
        md_path = os.path.join(output_dir, f"ABLATION_REPORT_{target_prediction.replace(' ', '_').replace('/', '_')}.md")
        
        md_content = f"# Ablation Study Report: {target_prediction}\n\n"
        md_content += "| Disabled Feature Group | Δ MCC | Δ Macro F1 | Δ Accuracy |\n"
        md_content += "|---|---|---|---|\n"
        
        for exp in relevant_exps:
            groups = ", ".join(exp.feature_groups_disabled)
            md_content += f"| {groups} | {exp.delta_mcc:+.4f} | {exp.delta_f1:+.4f} | {exp.delta_accuracy:+.4f} |\n"
            
        try:
            with open(md_path, "w") as f:
                f.write(md_content)
        except Exception:
            pass

ablation_framework = AblationFramework()
