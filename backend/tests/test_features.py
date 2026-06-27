import math
import numpy as np
import pandas as pd
from backend.physics.models import (
    PhysicsCharacterization,
    ThermalProfile,
    FlareClassification,
    EventCharacterization,
    GOESClass,
    PlasmaState,
    PhysicsQuality,
    PhysicsDerivedIndices,
    PhysicsProvenance
)
from backend.features.manager import feature_manager
from backend.features.repository.feature_store import feature_store
from backend.features.registry.feature_registry import feature_registry
from backend.features.validation.validation_engine import validation_engine
from backend.features.normalization.normalization_engine import normalization_engine
from backend.features.temporal.temporal_engine import temporal_engine
from backend.features.quality.quality_engine import quality_engine
from backend.features.lineage.lineage_engine import lineage_engine
from backend.features.statistics.statistics_engine import statistics_engine
from backend.features.prediction_targets.target_registry import target_registry
from backend.features.datasets.builder import dataset_builder

def get_mock_physics() -> PhysicsCharacterization:
    return PhysicsCharacterization(
        physics_product_id="PHY-20260627-001",
        master_id="FL-20260627-001",
        thermal=ThermalProfile(
            peak_temperature=15.5,
            emission_measure=48.2,
            heating_rate=0.5,
            cooling_rate=0.1,
            thermal_energy=1e30,
            temperature_gradient=0.2
        ),
        classification=FlareClassification(
            goes_class=GOESClass.M,
            goes_subclass="M2.3",
            peak_flux=2.3e-5
        ),
        characterization=EventCharacterization(
            rise_time=120.0,
            decay_time=360.0,
            duration=480.0,
            heating_duration=150.0,
            cooling_duration=330.0,
            maximum_derivative=1.5,
            peak_flux=2.3e-5,
            integrated_flux=10.5,
            peak_hard_xray=150.0,
            peak_soft_xray=80.0,
            signal_to_noise_ratio=25.0
        ),
        indices=PhysicsDerivedIndices(
            heating_index=5.0,
            cooling_index=3.0,
            energy_release_index=30.0,
            thermal_dominance=0.9,
            neupert_compliance=0.765,
            spectral_hardness=0.3125,
            impulsiveness_index=0.5
        )
    )

def test_registry():
    entry = feature_registry.get_feature("peak_temperature")
    assert entry is not None
    assert entry.feature_id == "F-THERM-001"
    assert entry.units == "MK"
    assert entry.normalization_strategy == "standard"

def test_validation():
    # Test valid range
    res = validation_engine.validate_features({"peak_temperature": 15.5})
    assert res["peak_temperature"].status == "VALID"

    # Test NaN invalid
    res = validation_engine.validate_features({"peak_temperature": float("nan")})
    assert res["peak_temperature"].status == "INVALID"

    # Test outside range degraded
    res = validation_engine.validate_features({"peak_temperature": 150.0})
    assert res["peak_temperature"].status == "DEGRADED"

def test_normalization():
    # standard scaling: (15.5 - 15.0) / 5.0 = 0.1
    val, meta = normalization_engine.normalize("peak_temperature", 15.5)
    assert val == 0.1
    assert meta.strategy == "standard"

    # minmax scaling: (120.0 - 0.0) / 10000.0 = 0.012
    val, meta = normalization_engine.normalize("rise_time", 120.0)
    assert round(val, 4) == 0.012
    assert meta.strategy == "minmax"

def test_temporal_engine():
    temporal_engine._history.clear()
    # Ingest 3 ticks of data
    temporal_engine.ingest_tick(solexs=1.0, helios=0.5, temp=10.0, timestamp_str="2026-06-27T00:00:00Z")
    temporal_engine.ingest_tick(solexs=2.0, helios=1.0, temp=11.0, timestamp_str="2026-06-27T00:00:01Z")
    feats = temporal_engine.ingest_tick(solexs=3.0, helios=1.5, temp=12.0, timestamp_str="2026-06-27T00:00:02Z")
    
    assert feats["solexs_flux_roll_mean_1m"] == 2.0
    assert feats["solexs_flux_roll_std_1m"] > 0.0
    assert feats["temp_roll_mean_1m"] == 11.0

def test_quality_engine():
    res = validation_engine.validate_features({"peak_temperature": 15.5, "rise_time": 120.0})
    report = quality_engine.calculate_quality(res)
    assert report.completeness == 1.0
    assert report.reliability == 1.0
    assert report.is_ml_ready is True

def test_lineage_engine():
    lineage_engine.record_lineage(
        feature_vector_id="FT-1",
        master_id="FL-1",
        physics_product_id="PHY-1",
        observation_ids=["OBS-1", "OBS-2"],
        validation_status="VALID",
        normalization_version="1.0.0",
        timestamp_str="2026-06-27T00:00:00Z"
    )
    lineage = lineage_engine.get_lineage("FT-1")
    assert len(lineage) == 5
    assert lineage[0].type == "Observation"
    assert lineage[-1].type == "FeatureVector"

def test_statistics_engine():
    mock_physics = get_mock_physics()
    feature_store.clear()
    
    statistics_engine.validation_runs = 0
    statistics_engine.validation_failures = 0
    statistics_engine.normalization_runs = 0
    statistics_engine.normalization_successes = 0

    feature_manager.extract_features(mock_physics)
    
    vectors = feature_store.get_all()
    stats = statistics_engine.compute_statistics(vectors)
    assert stats["total_records"] == 1
    assert stats["validation_failure_rate"] == 0.0
    assert stats["feature_stats"]["peak_temperature"]["mean"] == 15.5

def test_target_registry():
    targets = target_registry.get_all_targets()
    assert len(targets) > 0
    prob_target = target_registry.get_target("T-PROB-30M")
    assert prob_target is not None
    assert prob_target.variable_type == "classification"

def test_dataset_builder():
    mock_physics = get_mock_physics()
    feature_store.clear()
    # Add a vector to store
    feature_manager.extract_features(mock_physics)

    df, meta, report = dataset_builder.build_dataset()
    assert len(df) == 1
    assert "goes_class_next_1h" in df.columns
    assert "peak_flux_next_flare" in df.columns
    assert meta.total_samples == 1
    assert report.is_valid is True

    # Test export CSV
    csv_bytes = dataset_builder.export_dataset(df, "csv")
    assert len(csv_bytes) > 0
    assert b"goes_class_next_1h" in csv_bytes

    # Test export JSON
    json_bytes = dataset_builder.export_dataset(df, "json")
    assert len(json_bytes) > 0
    
    # Test export NumPy
    npy_bytes = dataset_builder.export_dataset(df, "numpy")
    assert len(npy_bytes) > 0
