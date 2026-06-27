from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from typing import List, Dict, Any, Optional
from datetime import datetime

from backend.features.repository.feature_store import feature_store
from backend.features.models import ScientificFeatureVector
from backend.features.registry.feature_registry import feature_registry
from backend.features.validation.validation_engine import validation_engine
from backend.features.quality.quality_engine import quality_engine
from backend.features.normalization.normalization_engine import normalization_engine
from backend.features.temporal.temporal_engine import temporal_engine
from backend.features.lineage.lineage_engine import lineage_engine
from backend.features.statistics.statistics_engine import statistics_engine
from backend.features.search.search_engine import search_engine
from backend.features.replay.replay_engine import replay_engine
from backend.features.prediction_targets.target_registry import target_registry
from backend.features.datasets.builder import dataset_builder

router = APIRouter(prefix="/features", tags=["features"])


@router.get("/vector/{feature_vector_id}", response_model=ScientificFeatureVector)
async def get_feature_vector(feature_vector_id: str):
    """Fetch full feature vector by ID."""
    vector = feature_store.get_by_id(feature_vector_id)
    if not vector:
        raise HTTPException(status_code=404, detail="Feature vector not found")
    return vector


@router.get("/by-physics/{physics_product_id}", response_model=ScientificFeatureVector)
async def get_features_by_physics(physics_product_id: str):
    """Resolve feature vector from physics product ID."""
    vector = feature_store.get_by_physics_id(physics_product_id)
    if not vector:
        raise HTTPException(status_code=404, detail="Feature vector not found for this physics_product_id")
    return vector


@router.get("/by-catalog/{master_id}", response_model=ScientificFeatureVector)
async def get_features_by_catalog(master_id: str):
    """Resolve feature vector from master catalog ID."""
    vector = feature_store.get_by_master_id(master_id)
    if not vector:
        raise HTTPException(status_code=404, detail="Feature vector not found for this master_id")
    return vector


@router.get("/registry")
async def get_registry():
    """Retrieve all registered features and their governance specifications."""
    return feature_registry.get_all_features()


@router.get("/validation")
async def get_validation_report(feature_vector_id: Optional[str] = None):
    """Get the runtime validation report for a feature vector."""
    if feature_vector_id:
        vector = feature_store.get_by_id(feature_vector_id)
        if not vector:
            raise HTTPException(status_code=404, detail="Feature vector not found")
        # Rerun validation on raw features
        return validation_engine.validate_features(vector.raw_features)
    
    # Return general validation metrics
    return {
        "validation_runs": statistics_engine.validation_runs,
        "validation_failures": statistics_engine.validation_failures,
        "failure_rate_percent": round((statistics_engine.validation_failures / statistics_engine.validation_runs * 100.0) if statistics_engine.validation_runs > 0 else 0.0, 2)
    }


@router.get("/quality")
async def get_quality_report(feature_vector_id: Optional[str] = None):
    """Retrieve quality report for a vector or quality trends history."""
    if feature_vector_id:
        vector = feature_store.get_by_id(feature_vector_id)
        if not vector:
            raise HTTPException(status_code=404, detail="Feature vector not found")
        return vector.quality_report
    
    return {
        "history": quality_engine.get_history(),
        "total_reports": len(quality_engine.get_history())
    }


@router.get("/statistics")
async def get_statistics():
    """Get feature store statistics, quality trends, and value distributions."""
    all_vectors = feature_store.get_all()
    return statistics_engine.compute_statistics(all_vectors)


@router.get("/search", response_model=List[ScientificFeatureVector])
async def get_search(
    category: Optional[str] = Query(None),
    is_ml_ready: Optional[bool] = Query(None),
    master_id: Optional[str] = Query(None),
    physics_product_id: Optional[str] = Query(None),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None)
):
    """Search for feature vectors based on filters."""
    return search_engine.search(
        category=category,
        is_ml_ready=is_ml_ready,
        master_id=master_id,
        physics_product_id=physics_product_id,
        start_time=start_time,
        end_time=end_time
    )


@router.get("/history", response_model=List[ScientificFeatureVector])
async def get_history(limit: int = 50):
    """Retrieve recent feature vectors."""
    vectors = feature_store.get_all()
    return list(reversed(vectors[-limit:]))


@router.get("/replay", response_model=List[ScientificFeatureVector])
async def get_replay(
    time_window: Optional[str] = Query(None),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    master_id: Optional[str] = Query(None)
):
    """Replay historical feature vectors for simulation or training."""
    return replay_engine.get_replay_dataset(
        time_window=time_window,
        start_time=start_time,
        end_time=end_time,
        master_id=master_id
    )


@router.get("/lineage/{feature_vector_id}")
async def get_lineage(feature_vector_id: str):
    """Retrieve complete scientific lineage for a feature vector."""
    lineage = lineage_engine.get_lineage(feature_vector_id)
    if not lineage:
        raise HTTPException(status_code=404, detail="Lineage not found for this vector ID")
    return lineage


@router.get("/versions")
async def get_versions():
    """Retrieve version configurations across all platform layers."""
    latest = feature_store.get_all()
    sample_vector = latest[-1] if latest else None
    
    return {
        "feature_pipeline_version": "1.0.0",
        "registry_version": "1.0.0",
        "validation_version": "1.0.0",
        "quality_version": "1.0.0",
        "normalization_version": "1.0.0",
        "source_physics_version": sample_vector.provenance.physics_product_version if sample_vector else "1.0.0",
        "source_pipeline_version": "1.0.0"
    }


@router.get("/normalization")
async def get_normalization_info():
    """Retrieve details of reference statistics and normalization strategies."""
    return {
        "reference_stats": normalization_engine._reference_stats,
        "strategies": {
            "rise_time": "minmax",
            "decay_time": "minmax",
            "duration": "minmax",
            "peak_flux": "minmax",
            "peak_temperature": "standard",
            "heating_index": "standard",
            "thermal_dominance": "none"
        }
    }


@router.get("/prediction-targets")
async def get_prediction_targets():
    """Retrieve registered forecast targets."""
    return target_registry.get_all_targets()


@router.get("/datasets/build")
async def get_dataset_build():
    """Compiles feature store vectors and labels, runs validations, and returns dataset metadata."""
    df, meta, report = dataset_builder.build_dataset()
    return {
        "metadata": meta,
        "validation_report": report
    }


@router.get("/datasets/export/{format_type}")
async def get_dataset_export(format_type: str):
    """Build and export the complete dataset in CSV, JSON, NumPy, or Parquet format."""
    df, _, _ = dataset_builder.build_dataset()
    try:
        data_bytes = dataset_builder.export_dataset(df, format_type)
        
        media_types = {
            "csv": "text/csv",
            "json": "application/json",
            "numpy": "application/octet-stream",
            "parquet": "application/octet-stream"
        }
        media = media_types.get(format_type.lower(), "application/octet-stream")
        
        headers = {
            "Content-Disposition": f"attachment; filename=aditya_l1_dataset.{format_type.lower()}"
        }
        
        return Response(content=data_bytes, media_type=media, headers=headers)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Export failed: {str(e)}")
