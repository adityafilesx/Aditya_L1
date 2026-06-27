from typing import List, Dict, Any, Tuple
import json
from datetime import datetime
import numpy as np
import pandas as pd
from pydantic import BaseModel
from backend.features.models import ScientificFeatureVector
from backend.features.repository.feature_store import feature_store

class LabelDefinition(BaseModel):
    label_id: str
    name: str
    description: str
    label_type: str  # "classification" or "regression"
    classes: List[str] = []


class DatasetMetadata(BaseModel):
    dataset_version: str = "1.0.0"
    feature_schema_version: str = "1.0.0"
    label_version: str = "1.0.0"
    generation_timestamp: str = ""
    source_feature_store_version: str = "1.0.0"
    total_samples: int = 0
    class_distribution: Dict[str, float] = {}


class DatasetValidationReport(BaseModel):
    is_valid: bool
    feature_completeness: float
    missing_ratio: float
    class_imbalance_ratio: float
    warnings: List[str] = []


class DatasetBuilder:
    """Orchestrates building, validating, and exporting ML-ready datasets."""

    def __init__(self):
        self.label_registry: Dict[str, LabelDefinition] = {}
        self._bootstrap_labels()

    def _bootstrap_labels(self) -> None:
        # Register forecast labels
        self.label_registry["L-CLASS-30M"] = LabelDefinition(
            label_id="L-CLASS-30M",
            name="goes_class_next_30m",
            description="GOES class label in the next 30 minutes",
            label_type="classification",
            classes=["A", "B", "C", "M", "X"]
        )
        self.label_registry["L-CLASS-1H"] = LabelDefinition(
            label_id="L-CLASS-1H",
            name="goes_class_next_1h",
            description="GOES class label in the next 1 hour",
            label_type="classification",
            classes=["A", "B", "C", "M", "X"]
        )
        self.label_registry["L-REG-FLUX"] = LabelDefinition(
            label_id="L-REG-FLUX",
            name="peak_flux_next_flare",
            description="Peak flux magnitude of next flare",
            label_type="regression"
        )

    def generate_labels(self, vectors: List[ScientificFeatureVector]) -> List[Dict[str, Any]]:
        """Simulate/calculate forecast labels for a list of feature vectors.

        In production, this looks ahead at subsequent chronologically ordered events
        to compute actual outcomes (A/B/C/M/X classification class or peak flux regression target).
        """
        labels = []
        for i, vec in enumerate(vectors):
            # For simulation/mock purposes, we derive target label from indices or peak_flux
            # e.g., if peak_flux is large, next flare class has M or X probability
            peak = vec.peak_flux
            
            if peak >= 1e-4:
                goes_class = "X"
                flux_val = 2e-4
            elif peak >= 1e-5:
                goes_class = "M"
                flux_val = 5e-5
            elif peak >= 1e-6:
                goes_class = "C"
                flux_val = 3e-6
            else:
                goes_class = "B"
                flux_val = 5e-7

            labels.append({
                "master_id": vec.master_id,
                "goes_class_next_30m": goes_class,
                "goes_class_next_1h": goes_class,
                "peak_flux_next_flare": flux_val,
            })
        return labels

    def build_dataset(self) -> Tuple[pd.DataFrame, DatasetMetadata, DatasetValidationReport]:
        """Combine feature store vectors and generated labels into a single dataset DataFrame."""
        vectors = feature_store.get_all()
        if not vectors:
            # Fallback empty dataframe
            df = pd.DataFrame(columns=["feature_vector_id", "goes_class_next_1h", "peak_flux_next_flare"])
            meta = DatasetMetadata(generation_timestamp=datetime.utcnow().isoformat() + "Z")
            report = DatasetValidationReport(is_valid=False, feature_completeness=0.0, missing_ratio=1.0, class_imbalance_ratio=0.0, warnings=["No features present in Feature Store"])
            return df, meta, report

        # Extract features
        feat_data = []
        for v in vectors:
            d = v.to_dict()
            d["feature_vector_id"] = v.feature_vector_id
            d["master_id"] = v.master_id
            feat_data.append(d)
        
        df_feat = pd.DataFrame(feat_data)
        
        # Extract labels
        labels = self.generate_labels(vectors)
        df_labels = pd.DataFrame(labels)

        # Merge features and labels
        df_merged = pd.merge(df_feat, df_labels, on="master_id", how="inner")

        # Compute metadata
        total_samples = len(df_merged)
        class_counts = df_merged["goes_class_next_1h"].value_counts().to_dict()
        class_dist = {str(k): float(v) / total_samples for k, v in class_counts.items()}

        metadata = DatasetMetadata(
            generation_timestamp=datetime.utcnow().isoformat() + "Z",
            total_samples=total_samples,
            class_distribution=class_dist
        )

        # Perform validation checks
        missing_count = df_merged.isna().sum().sum()
        total_cells = df_merged.size
        missing_ratio = float(missing_count / total_cells) if total_cells > 0 else 1.0
        completeness = 1.0 - missing_ratio

        # Class imbalance check (ratio of largest class to smallest class)
        imbalance_ratio = 1.0
        warnings = []
        if class_counts:
            max_class = max(class_counts.values())
            min_class = min(class_counts.values())
            imbalance_ratio = max_class / min_class if min_class > 0 else float(max_class)
            if imbalance_ratio > 4.0:
                warnings.append(f"High class imbalance detected (Ratio: {imbalance_ratio:.2f})")

        if completeness < 0.95:
            warnings.append(f"Completeness is below target: {completeness * 100.0:.2f}%")

        report = DatasetValidationReport(
            is_valid=completeness >= 0.90 and imbalance_ratio < 20.0,
            feature_completeness=round(completeness, 4),
            missing_ratio=round(missing_ratio, 4),
            class_imbalance_ratio=round(imbalance_ratio, 2),
            warnings=warnings
        )

        return df_merged, metadata, report

    def export_dataset(self, df: pd.DataFrame, format_type: str) -> bytes:
        """Export dataset to bytes in CSV, NumPy, Parquet, or JSON format."""
        fmt = format_type.lower()
        if fmt == "csv":
            return df.to_csv(index=False).encode("utf-8")
        elif fmt == "json":
            return df.to_json(orient="records", indent=2).encode("utf-8")
        elif fmt == "numpy":
            # Convert dataframe numeric fields to numpy array
            numeric_df = df.select_dtypes(include=[np.number])
            array = numeric_df.to_numpy()
            from io import BytesIO
            io_buf = BytesIO()
            np.save(io_buf, array)
            return io_buf.getvalue()
        elif fmt == "parquet":
            try:
                # Direct parquet export via pyarrow / pandas
                return df.to_parquet(index=False)
            except Exception as e:
                # Fallback to csv if pyarrow is broken or not installed
                return f"PARQUET EXPORT ERROR: {str(e)}. Fallback to CSV.\n".encode("utf-8") + df.to_csv(index=False).encode("utf-8")
        
        raise ValueError(f"Unsupported format type: {format_type}")


# Global singleton instance
dataset_builder = DatasetBuilder()
