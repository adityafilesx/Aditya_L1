from typing import Dict, List, Any
import numpy as np

class FeatureStatisticsEngine:
    """Computes distributions, outliers, missing rates, and quality trends for all features."""

    def __init__(self):
        self.validation_runs = 0
        self.validation_failures = 0
        self.normalization_runs = 0
        self.normalization_successes = 0

    def record_validation(self, is_valid: bool) -> None:
        self.validation_runs += 1
        if not is_valid:
            self.validation_failures += 1

    def record_normalization(self, success: bool) -> None:
        self.normalization_runs += 1
        if success:
            self.normalization_successes += 1

    def compute_statistics(self, all_vectors: List[Any]) -> Dict[str, Any]:
        """Compute summary statistics for all features currently stored."""
        if not all_vectors:
            return {
                "total_records": 0,
                "validation_failure_rate": 0.0,
                "normalization_success_rate": 100.0,
                "feature_stats": {}
            }

        total_records = len(all_vectors)
        fail_rate = (self.validation_failures / self.validation_runs * 100.0) if self.validation_runs > 0 else 0.0
        norm_rate = (self.normalization_successes / self.normalization_runs * 100.0) if self.normalization_runs > 0 else 100.0

        # Extract values for registered features
        feature_keys = [
            "rise_time", "decay_time", "duration", "peak_flux", 
            "peak_temperature", "heating_index", "thermal_dominance"
        ]

        feature_stats = {}
        for key in feature_keys:
            vals = []
            for vec in all_vectors:
                val = getattr(vec, key, None)
                if val is not None and not np.isnan(val):
                    vals.append(val)

            if vals:
                mean = float(np.mean(vals))
                std = float(np.std(vals))
                q25, q75 = np.percentile(vals, [25, 75])
                iqr = q75 - q25
                # Outlier rule: 1.5 * IQR bounds
                lower_bound = q25 - 1.5 * iqr
                upper_bound = q75 + 1.5 * iqr
                outliers = [v for v in vals if v < lower_bound or v > upper_bound]
                outlier_pct = (len(outliers) / len(vals)) * 100.0

                feature_stats[key] = {
                    "mean": round(mean, 4),
                    "median": round(float(np.median(vals)), 4),
                    "min": round(float(np.min(vals)), 4),
                    "max": round(float(np.max(vals)), 4),
                    "std": round(std, 4),
                    "missing_pct": round(((total_records - len(vals)) / total_records) * 100.0, 2),
                    "outlier_pct": round(outlier_pct, 2)
                }
            else:
                feature_stats[key] = {
                    "mean": 0.0, "median": 0.0, "min": 0.0, "max": 0.0, "std": 0.0,
                    "missing_pct": 100.0, "outlier_pct": 0.0
                }

        return {
            "total_records": total_records,
            "validation_failure_rate": round(fail_rate, 2),
            "normalization_success_rate": round(norm_rate, 2),
            "feature_stats": feature_stats
        }


# Global singleton instance
statistics_engine = FeatureStatisticsEngine()
