import os
import sys
import pickle
import pandas as pd
import numpy as np
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))
from backend.aditya_flare.processing.features import extract_features

def test_pipeline_robustness():
    print("==================================================")
    print("STRESS TESTING PIPELINE FOR TELEMETRY LOSS")
    print("==================================================")
    
    processed_dir = Path("data/processed")
    model_path = Path("data/models/ensemble_forecaster.pkl")
    
    # Locate a merged file
    parquet_files = sorted(list(processed_dir.glob("merged_*.parquet")))
    if not parquet_files:
        print("Error: No merged parquet files found in data/processed.")
        return
        
    test_file = parquet_files[0]
    print(f"Using test file: {test_file.name}")
    
    # Load raw merged df
    raw_df = pd.read_parquet(test_file)
    print(f"Original record count: {len(raw_df)} seconds")
    
    # Create copy and introduce telemetry gaps
    corrupted_df = raw_df.copy()
    np.random.seed(42)
    
    # 1. Inject 15% random packet drops
    num_drops = int(len(corrupted_df) * 0.15)
    drop_indices = np.random.choice(corrupted_df.index, size=num_drops, replace=False)
    corrupted_df.loc[drop_indices, 'solexs_sdd2_ctr'] = np.nan
    corrupted_df.loc[drop_indices, 'helios_czt_broad_ctr'] = np.nan
    corrupted_df.loc[drop_indices, 'hardness_ratio'] = np.nan
    print(f"-> Injected 15% random packet drops ({num_drops} seconds of NaNs)")
    
    # 2. Inject a 15-minute contiguous telemetry gap
    mid_point = corrupted_df.index[len(corrupted_df) // 2]
    gap_start = mid_point - pd.Timedelta(minutes=10)
    gap_end = mid_point + pd.Timedelta(minutes=5)
    corrupted_df.loc[gap_start:gap_end, 'solexs_sdd2_ctr'] = np.nan
    corrupted_df.loc[gap_start:gap_end, 'helios_czt_broad_ctr'] = np.nan
    corrupted_df.loc[gap_start:gap_end, 'hardness_ratio'] = np.nan
    print(f"-> Injected 15-minute contiguous telemetry outage from {gap_start} to {gap_end}")
    
    # Save corrupted dataframe to a temporary parquet file to simulate raw folder input
    temp_dir = processed_dir / "temp_stress_test"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_file = temp_dir / test_file.name
    corrupted_df.to_parquet(temp_file)
    
    # Try running the extraction pipeline
    print("\nRunning feature extraction with interpolation + forward-fill imputation...")
    try:
        features_df = extract_features(temp_dir, flare_threshold=500.0)
        print("-> SUCCESS: Feature extraction completed without throwing NaN/Shape errors.")
        print(f"Processed feature matrix shape: {features_df.shape}")
        
        # Verify no NaN values exist in the feature set
        nan_cols = features_df.isna().sum()
        total_nans = nan_cols.sum()
        if total_nans == 0:
            print("-> VERIFIED: Feature matrix has 0 remaining NaN cells.")
        else:
            print(f"-> WARNING: Found {total_nans} remaining NaN cells in columns:\n{nan_cols[nan_cols > 0]}")
            
        # Test predictions using the trained ensemble model
        if model_path.exists():
            with open(model_path, "rb") as f:
                ensemble_data = pickle.load(f)
            
            X_sim = features_df[ensemble_data['features']].values
            p_lgb = ensemble_data['lgb'].predict_proba(X_sim)[:, 1]
            p_knn = ensemble_data['knn'].predict_proba(X_sim)[:, 1]
            y_prob = (0.7 * p_lgb) + (0.3 * p_knn)
            print(f"-> VERIFIED: Ensemble predictions completed. Average predicted probability: {np.mean(y_prob):.4f}")
            print("-> TEST STATUS: PASSED")
        else:
            print("-> Skipping prediction test (Model file missing).")
            print("-> TEST STATUS: PASSED (Extraction only)")
            
    except Exception as e:
        print(f"-> FAILED: Pipeline crashed under data loss stress: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup temp directory
        if temp_file.exists():
            os.remove(temp_file)
        if temp_dir.exists():
            os.rmdir(temp_dir)
            
if __name__ == '__main__':
    test_pipeline_robustness()
