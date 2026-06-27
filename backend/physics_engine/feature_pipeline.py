import time
import pandas as pd
import logging
from pathlib import Path

# Original feature extractor
from backend.aditya_flare.processing.features import extract_features as original_extract_features

# New physics engine modules
from backend.physics_engine.statistics import extract_statistical_features
from backend.physics_engine.entropy import extract_entropy_features
from backend.physics_engine.wavelets import extract_wavelet_features
from backend.physics_engine.spectral import extract_spectral_features
from backend.physics_engine.thermodynamics import extract_thermodynamic_features
from backend.physics_engine.neupert import extract_neupert_features
from backend.physics_engine.event_segmentation import segment_events_and_timeline
import concurrent.futures

logger = logging.getLogger(__name__)

def extract_physics_features(processed_dir: str, max_days: int = None, flare_threshold: float = 500.0) -> pd.DataFrame:
    """
    Master Physics Feature Aggregator.
    Calls the original extract_features() and enriches it with the Physics Feature Engine.
    """
    logger.info("Starting Phase 3 Physics-Informed Feature Extraction...")
    start_time = time.time()
    
    # 1. Base ML Features (Unchanged)
    df = original_extract_features(processed_dir, max_days=max_days, flare_threshold=flare_threshold)
    
    cols_to_process = ['solexs_sdd2_ctr', 'helios_czt_broad_ctr']
    window = 15
    
    # 2. Physics Feature Engineering
    logger.info("Extracting Physics Features Asynchronously...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        f_stat = executor.submit(extract_statistical_features, df.copy(), cols_to_process, window)
        f_therm = executor.submit(extract_thermodynamic_features, df.copy(), 'solexs_sdd2_ctr', 'helios_czt_broad_ctr', window)
        f_neup = executor.submit(extract_neupert_features, df.copy(), 'solexs_sdd2_ctr', 'helios_czt_broad_ctr', window)
        f_ent = executor.submit(extract_entropy_features, df.copy(), cols_to_process, window)
        f_wav = executor.submit(extract_wavelet_features, df.copy(), cols_to_process, window)
        f_spec = executor.submit(extract_spectral_features, df.copy(), cols_to_process, window)
        
        df_stat = f_stat.result()
        df_therm = f_therm.result()
        df_neup = f_neup.result()
        df_ent = f_ent.result()
        df_wav = f_wav.result()
        df_spec = f_spec.result()
        
    def get_new_cols(original, modified):
        return modified[[c for c in modified.columns if c not in original.columns]]
        
    df = pd.concat([
        df,
        get_new_cols(df, df_stat),
        get_new_cols(df, df_therm),
        get_new_cols(df, df_neup),
        get_new_cols(df, df_ent),
        get_new_cols(df, df_wav),
        get_new_cols(df, df_spec)
    ], axis=1)
    
    logger.info("Extracting Morphology & Segmentation...")
    df = segment_events_and_timeline(df, flux_col='solexs_sdd2_ctr', threshold=100.0)
    
    # Drop NaNs from new rolling operations
    df = df.dropna()
    
    # Feature Store & Versioning
    store_dir = Path("data/feature_store")
    store_dir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(store_dir / "features_v3.1.parquet")
    logger.info("Features saved to local feature store (v3.1)")
    
    elapsed = time.time() - start_time
    logger.info(f"Physics Engine Complete. Final Matrix Shape: {df.shape}. Total Execution Time: {elapsed:.2f}s")
    
    # Verify constraint: For real-time, one row should take <100ms. 
    # Here we are processing thousands of rows, so average per-row time should be <100ms.
    ms_per_row = (elapsed / max(1, len(df))) * 1000
    logger.info(f"Performance Check: {ms_per_row:.2f} ms/row (Target: <100ms/row)")
    
    return df
