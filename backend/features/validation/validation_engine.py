from typing import Dict, Any, List
import math
from pydantic import BaseModel
from backend.features.registry.feature_registry import feature_registry

class ValidationResultDetail(BaseModel):
    status: str  # "VALID", "WARNING", "DEGRADED", "INVALID"
    message: str
    value: float


class FeatureValidationEngine:
    """Performs runtime validations on extracted features based on registry rules."""

    def validate_features(self, raw_features: Dict[str, float]) -> Dict[str, ValidationResultDetail]:
        results: Dict[str, ValidationResultDetail] = {}

        for name, value in raw_features.items():
            entry = feature_registry.get_feature(name)
            
            # If not registered, it is warning/degraded
            if not entry:
                results[name] = ValidationResultDetail(
                    status="WARNING",
                    message="Feature is not registered in the Feature Registry.",
                    value=value
                )
                continue

            # 1. NaN and Inf checks
            if math.isnan(value):
                results[name] = ValidationResultDetail(
                    status="INVALID",
                    message="Value is NaN.",
                    value=value
                )
                continue
                
            if math.isinf(value):
                results[name] = ValidationResultDetail(
                    status="INVALID",
                    message="Value is Infinite.",
                    value=value
                )
                continue

            # 2. Allowed Range checks
            min_val, max_val = entry.allowed_range
            if value < min_val:
                results[name] = ValidationResultDetail(
                    status="INVALID" if min_val >= 0 and "min_value" in entry.quality_rules else "DEGRADED",
                    message=f"Value {value} is below allowed range minimum {min_val}.",
                    value=value
                )
                continue
                
            if value > max_val:
                results[name] = ValidationResultDetail(
                    status="DEGRADED",
                    message=f"Value {value} exceeds allowed range maximum {max_val}.",
                    value=value
                )
                continue

            # Default valid case
            results[name] = ValidationResultDetail(
                status="VALID",
                message="Feature satisfies all validation constraints.",
                value=value
            )

        return results


# Global singleton instance
validation_engine = FeatureValidationEngine()
