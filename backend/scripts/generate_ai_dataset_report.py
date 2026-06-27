import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))
from backend.aditya_flare.ai_engine.dataset import TemporalFlareDataset, DataSplitter, generate_dataset_report

def main():
    print("Loading data...")
    catalog_path = Path("data/processed/master_flare_catalog.csv")
    features_path = Path("data/processed/aligned_goes_solexs.parquet")
    
    df_catalog = pd.read_csv(catalog_path)
    df_features = pd.read_parquet(features_path)
    
    # Ensure datetime indices
    df_features.index = pd.to_datetime(df_features.index)
    
    # Create target columns if they don't exist
    if 'class_target' not in df_features.columns:
        # Simple binary classification based on flux threshold (e.g. > 1e-6)
        df_features['class_target'] = (df_features['goes_xrsa_flux'] > 1e-6).astype(int)
    
    feature_cols = ['solexs_sdd2_ctr', 'hardness_ratio', 'goes_xrsa_flux', 'goes_xrsb_flux']
    
    # Split flares by Cycle 24/25
    flare_ids = df_catalog['flare_id'].tolist()
    train_flares, val_flares = DataSplitter.cross_cycle_split(df_catalog, cycle_threshold='2024-08-01')
    
    print(f"Train Flares: {len(train_flares)}, Val Flares: {len(val_flares)}")
    
    print("Generating train dataset...")
    train_dataset = TemporalFlareDataset(
        df_features=df_features, 
        df_catalog=df_catalog, 
        flare_ids=train_flares, 
        feature_cols=feature_cols,
        history_window_mins=60,
        prediction_horizon_mins=30,
        cadence_mins=1,
        max_seq_len=120
    )
    
    print("Generating val dataset...")
    val_dataset = TemporalFlareDataset(
        df_features=df_features, 
        df_catalog=df_catalog, 
        flare_ids=val_flares, 
        feature_cols=feature_cols,
        history_window_mins=60,
        prediction_horizon_mins=30,
        cadence_mins=1,
        max_seq_len=120
    )
    
    train_report = generate_dataset_report(train_dataset)
    val_report = generate_dataset_report(val_dataset)
    
    final_report = "# Phase 4: Temporal AI Dataset Report\n\n"
    final_report += "## Train Set (Cross-Cycle Split)\n"
    final_report += train_report
    final_report += "\n## Validation Set\n"
    final_report += val_report
    
    out_dir = Path("data/evaluation")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "Dataset_Report.md"
    
    with open(out_path, "w") as f:
        f.write(final_report)
        
    print(f"Report saved to {out_path}")

if __name__ == "__main__":
    main()
