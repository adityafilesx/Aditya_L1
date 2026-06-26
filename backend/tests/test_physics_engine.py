import pytest
import numpy as np
import pandas as pd
from physics_engine.statistics import extract_statistical_features
from physics_engine.entropy import extract_entropy_features, shannon_entropy
from physics_engine.wavelets import extract_wavelet_features
from physics_engine.spectral import extract_spectral_features
from physics_engine.thermodynamics import extract_thermodynamic_features
from physics_engine.neupert import compute_neupert_score
from physics_engine.event_segmentation import segment_events_and_timeline
from physics_engine.feature_pipeline import extract_physics_features

@pytest.fixture
def dummy_dataframe():
    np.random.seed(42)
    # 50 rows of data
    df = pd.DataFrame({
        'solexs_sdd2_ctr': np.random.lognormal(mean=2.0, sigma=1.0, size=50) * 10,
        'helios_czt_broad_ctr': np.random.lognormal(mean=1.5, sigma=0.8, size=50) * 5
    })
    # Inject a flare shape
    x = np.arange(50)
    flare = 1000 * np.exp(-((x - 25)**2) / 20)
    df['solexs_sdd2_ctr'] += flare
    df['helios_czt_broad_ctr'] += flare * 0.5
    return df

def test_statistics(dummy_dataframe):
    df_out = extract_statistical_features(dummy_dataframe, ['solexs_sdd2_ctr'], window=5)
    assert 'solexs_sdd2_ctr_roll_mean_5' in df_out.columns
    assert 'solexs_sdd2_ctr_roll_mad_5' in df_out.columns
    assert 'solexs_sdd2_ctr_roll_skew_5' in df_out.columns
    assert len(df_out) == 50

def test_entropy(dummy_dataframe):
    df_out = extract_entropy_features(dummy_dataframe, ['solexs_sdd2_ctr'], window=10)
    assert 'solexs_sdd2_ctr_shannon_entropy_10' in df_out.columns
    assert 'solexs_sdd2_ctr_sample_entropy_10' in df_out.columns

def test_wavelets(dummy_dataframe):
    df_out = extract_wavelet_features(dummy_dataframe, ['solexs_sdd2_ctr'], window=16)
    assert 'solexs_sdd2_ctr_wavelet_energy_16' in df_out.columns
    assert 'solexs_sdd2_ctr_hf_burst_intensity_16' in df_out.columns

def test_spectral(dummy_dataframe):
    df_out = extract_spectral_features(dummy_dataframe, ['solexs_sdd2_ctr'], window=16)
    assert 'solexs_sdd2_ctr_spec_centroid_16' in df_out.columns
    assert 'solexs_sdd2_ctr_spec_flatness_16' in df_out.columns

def test_thermodynamics(dummy_dataframe):
    df_out = extract_thermodynamic_features(dummy_dataframe, window=5)
    assert 'estimated_temperature_mk' in df_out.columns
    assert 'thermo_confidence' in df_out.columns
    assert df_out['estimated_em_norm'].isnull().all() # Should be NaN without XSPEC

def test_neupert_score():
    soft = np.array([1, 2, 4, 8, 16])
    hard = np.array([1, 2, 4, 8, 16])
    score = compute_neupert_score(soft, hard)
    assert score > 0.9 # High correlation

def test_morphology(dummy_dataframe):
    df_out = segment_events_and_timeline(dummy_dataframe, threshold=100)
    assert 'physics_timeline' in df_out.columns
    assert 'flare_morphology' in df_out.columns
    assert 'Peak' in df_out['physics_timeline'].values
    assert 'Background' in df_out['physics_timeline'].values

def test_feature_pipeline(dummy_dataframe):
    import os
    # Just need to check it runs without crashing and creates a parquet file
    # Ensure processed_dir logic is mocked or we provide a valid path
    pass

