from typing import Dict, List, Any
from pydantic import BaseModel
from datetime import datetime
from backend.features.validation.validation_engine import ValidationResultDetail

class FeatureQualityReport(BaseModel):
    completeness: float  # 0.0 to 1.0
    reliability: float   # 0.0 to 1.0
    consistency: float   # 0.0 to 1.0
    freshness_s: float
    overall_quality_score: float  # 0.0 to 1.0
    is_ml_ready: bool


class FeatureQualityEngine:
    """Calculates scientific quality and readiness scores for feature vectors."""

    def __init__(self):
        self._history: List[Dict[str, Any]] = []

    def calculate_quality(
        self, 
        validation_results: Dict[str, ValidationResultDetail],
        peak_time_str: str | None = None
    ) -> FeatureQualityReport:
        total_features = len(validation_results)
        if total_features == 0:
            return FeatureQualityReport(
                completeness=0.0,
                reliability=0.0,
                consistency=1.0,
                freshness_s=0.0,
                overall_quality_score=0.0,
                is_ml_ready=False
            )

        # 1. Completeness: fraction of features that are NOT NaN/Inf/INVALID
        valid_count = sum(1 for r in validation_results.values() if r.status != "INVALID")
        completeness = valid_count / total_features

        # 2. Reliability: based on warning / degradation weights
        # VALID = 1.0, WARNING = 0.8, DEGRADED = 0.5, INVALID = 0.0
        reliability_scores = []
        for r in validation_results.values():
            if r.status == "VALID":
                reliability_scores.append(1.0)
            elif r.status == "WARNING":
                reliability_scores.append(0.8)
            elif r.status == "DEGRADED":
                reliability_scores.append(0.5)
            else:
                reliability_scores.append(0.0)
        reliability = sum(reliability_scores) / total_features

        # 3. Freshness calculation (relative to current peak time)
        freshness_s = 0.0
        if peak_time_str:
            try:
                peak_dt = datetime.fromisoformat(peak_time_str.replace("Z", "+00:00"))
                freshness_s = (datetime.utcnow() - peak_dt.replace(tzinfo=None)).total_seconds()
            except:
                pass

        # 4. Consistency: e.g., cross feature ranges/checks
        consistency = 1.0
        # Check rise_time + decay_time <= duration bounds if they exist
        if "rise_time" in validation_results and "decay_time" in validation_results and "duration" in validation_results:
            rise = validation_results["rise_time"].value
            decay = validation_results["decay_time"].value
            dur = validation_results["duration"].value
            if abs((rise + decay) - dur) > 5.0:  # Allow small floating point offset
                consistency = 0.7

        # 5. Overall Score
        overall = (completeness * 0.4) + (reliability * 0.4) + (consistency * 0.2)
        is_ml_ready = (completeness >= 0.95) and (reliability >= 0.8) and (consistency >= 0.7)

        report = FeatureQualityReport(
            completeness=round(completeness, 4),
            reliability=round(reliability, 4),
            consistency=round(consistency, 4),
            freshness_s=round(freshness_s, 2),
            overall_quality_score=round(overall, 4),
            is_ml_ready=is_ml_ready
        )

        # Log to history
        self._history.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "score": report.overall_quality_score,
            "is_ml_ready": report.is_ml_ready
        })
        if len(self._history) > 1000:
            self._history.pop(0)

        return report

    def get_history(self) -> List[Dict[str, Any]]:
        return self._history


# Global singleton instance
quality_engine = FeatureQualityEngine()
