import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from backend.ml.registry.model_registry import model_registry, ModelMetadata
from backend.ml.selection.selection_engine import selection_engine

class PromotionLog(BaseModel):
    promotion_id: str
    model_id: str
    previous_stage: str
    new_stage: str
    reason: str
    timestamp: str
    reviewer: str

class PromotionManager:
    """Manages model lifecycle promotions and logging."""
    def __init__(self, storage_path: str = "data/ml_promotions.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.logs: List[PromotionLog] = []
        self._load_logs()

    def _load_logs(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    self.logs = [PromotionLog(**log) for log in data]
            except Exception:
                self.logs = []

    def _save_logs(self) -> None:
        with open(self.storage_path, "w") as f:
            json.dump([log.dict() for log in self.logs], f, indent=2)

    def promote_model(self, model_id: str, new_stage: str, reason: str, reviewer: str = "Automated System", override_reference: bool = False) -> bool:
        model = model_registry.get_model(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found in registry.")

        previous_stage = model.deployment_stage
        
        try:
            model_registry.update_deployment_stage(model_id, new_stage, override_reference=override_reference)
        except ValueError as e:
            # Generate rejection report
            self._generate_rejection_report(model, str(e), reviewer)
            return False

        # Log promotion
        log = PromotionLog(
            promotion_id=f"promo_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{model_id[:6]}",
            model_id=model_id,
            previous_stage=previous_stage,
            new_stage=new_stage,
            reason=reason,
            timestamp=datetime.utcnow().isoformat(),
            reviewer=reviewer
        )
        self.logs.append(log)
        self._save_logs()
        
        if new_stage == "ACTIVE":
            self._generate_acceptance_report(model, reason, reviewer)
            
        return True
        
    def _generate_acceptance_report(self, model: ModelMetadata, reason: str, reviewer: str):
        report_path = f"/Users/aditya1981/.gemini/antigravity-ide/brain/4be69a0e-4cb8-4457-b7dc-8b8a07b18a03/MODEL_ACCEPTANCE_REPORT_{model.model_id}.md"
        content = f"""# Model Acceptance Report: {model.model_name}

## Promotion Summary
- **Model ID**: {model.model_id}
- **Algorithm**: {model.algorithm}
- **Implementation**: {model.implementation_classification}
- **Reviewer**: {reviewer}
- **Decision**: ACCEPTED
- **Rationale**: {reason}

## Metrics & Calibration
- **Accuracy**: {model.evaluation_metrics.get('accuracy', 'N/A')}
- **Macro F1**: {model.evaluation_metrics.get('macro_f1', 'N/A')}
- **MCC**: {model.evaluation_metrics.get('mcc', 'N/A')}
- **Expected Calibration Error (ECE)**: {model.evaluation_metrics.get('ece', 'N/A')}
"""
        try:
            with open(report_path, "w") as f:
                f.write(content)
        except Exception:
            pass
            
    def _generate_rejection_report(self, model: ModelMetadata, reason: str, reviewer: str):
        report_path = f"/Users/aditya1981/.gemini/antigravity-ide/brain/4be69a0e-4cb8-4457-b7dc-8b8a07b18a03/MODEL_REJECTION_REPORT_{model.model_id}.md"
        content = f"""# Model Rejection Report: {model.model_name}

## Promotion Summary
- **Model ID**: {model.model_id}
- **Implementation**: {model.implementation_classification}
- **Reviewer**: {reviewer}
- **Decision**: REJECTED
- **Rationale**: {reason}

## Metrics
- **Accuracy**: {model.evaluation_metrics.get('accuracy', 'N/A')}
- **MCC**: {model.evaluation_metrics.get('mcc', 'N/A')}
"""
        try:
            with open(report_path, "w") as f:
                f.write(content)
        except Exception:
            pass

promotion_manager = PromotionManager()
