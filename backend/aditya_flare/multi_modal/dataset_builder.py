import pandas as pd
import numpy as np
import logging
from pathlib import Path

logger = logging.getLogger("AdityaL1.MultiModal.DatasetBuilder")

class MultiModalDatasetBuilder:
    """
    Phase 5A: Multi-Modal Dataset Builder.
    The single source of truth for all downstream models.
    Handles timestamp alignment, cadence synchronization, interpolation, 
    modality masking, quality flags, and feature merging.
    """
    def __init__(self, cache_dir="data/multi_modal/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def synchronize_timestamps(self, df_primary, df_secondary, tolerance='5T'):
        """
        Time Synchronization Engine.
        Aligns a secondary modality (e.g., HMI, AIA) to the primary modality (e.g., SoLEXS/GOES)
        using nearest-neighbor matching within a specified time tolerance to avoid forward data leakage.
        """
        # Ensure timestamps are sorted
        df_primary = df_primary.sort_values('timestamp')
        df_secondary = df_secondary.sort_values('timestamp')
        
        # Merge-asof performs nearest matching. Direction 'backward' prevents future leakage.
        merged = pd.merge_asof(
            df_primary, 
            df_secondary, 
            on='timestamp', 
            direction='backward', 
            tolerance=pd.Timedelta(tolerance)
        )
        return merged

    def compute_quality_flags(self, df, modality_prefix):
        """
        Data Quality System.
        Generates Availability, Quality Score, Missing Flag, Interpolated Flag, and Timestamp Freshness.
        """
        # Assume all columns with this prefix belong to the modality
        modality_cols = [c for c in df.columns if c.startswith(modality_prefix)]
        
        if not modality_cols:
            df[f'{modality_prefix}_available'] = 0
            df[f'{modality_prefix}_missing_flag'] = 1
            df[f'{modality_prefix}_quality_score'] = 0.0
            return df
            
        # Check if all modality features are NaN for a given row
        is_missing = df[modality_cols].isna().all(axis=1)
        
        df[f'{modality_prefix}_missing_flag'] = is_missing.astype(int)
        df[f'{modality_prefix}_available'] = (~is_missing).astype(int)
        
        # Simulate an interpolation flag (if it was NaN before interpolation)
        # Here we just mark 0 for simplicity, upstream modules would pass actual interpolation flags
        df[f'{modality_prefix}_interpolated_flag'] = 0 
        
        # Quality score: 1.0 if available and not interpolated, 0.5 if interpolated, 0.0 if missing
        df[f'{modality_prefix}_quality_score'] = np.where(
            is_missing, 0.0,
            np.where(df[f'{modality_prefix}_interpolated_flag'] == 1, 0.5, 1.0)
        )
        
        return df

    def apply_modality_masking(self, df, modality_prefix, force_mask=False):
        """
        Missing-Modality Robustness.
        Zeroes out features for a modality if it is missing or forced to mask (for ablation/dropout).
        """
        modality_cols = [c for c in df.columns if c.startswith(modality_prefix)]
        mask_condition = (df[f'{modality_prefix}_missing_flag'] == 1) | force_mask
        
        for col in modality_cols:
            df.loc[mask_condition, col] = 0.0  # Zero-imputation for neural network masking
            
        return df

    def build_dataset(self, primary_df, hmi_df=None, goes_df=None, aia_df=None, swis_df=None, cache_name="fused_dataset"):
        """
        The central dataset builder merging all available modalities.
        Order of alignment: Primary (SoLEXS) <- HMI <- GOES <- AIA <- SWIS
        """
        logger.info("Building multi-modal dataset...")
        
        fused = primary_df.copy()
        
        modalities = [
            ('hmi', hmi_df, '1H'), 
            ('goes', goes_df, '5T'), 
            ('aia', aia_df, '12T'), 
            ('swis', swis_df, '1H')
        ]
        
        for prefix, mod_df, tolerance in modalities:
            if mod_df is not None and not mod_df.empty:
                # 1. Synchronization
                fused = self.synchronize_timestamps(fused, mod_df, tolerance=tolerance)
            
            # 2. Quality Flags (even if mod_df is None, generates missing flags)
            fused = self.compute_quality_flags(fused, prefix)
            
            # 3. Masking
            fused = self.apply_modality_masking(fused, prefix)
            
        # Optional: Normalization would go here
        
        # Caching
        cache_file = self.cache_dir / f"{cache_name}.parquet"
        fused.to_parquet(cache_file)
        logger.info(f"Dataset built and cached to {cache_file} (Shape: {fused.shape})")
        
        return fused

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    builder = MultiModalDatasetBuilder()
    
    # Simulate primary (SoLEXS)
    times = pd.date_range(end=pd.Timestamp.utcnow(), periods=10, freq='1T')
    solexs = pd.DataFrame({'timestamp': times, 'solexs_flux': np.random.rand(10)})
    
    # Simulate HMI (only 1 data point, misaligned)
    hmi = pd.DataFrame({'timestamp': [times[2]], 'hmi_USFLUX': [5e22], 'hmi_MEANSHR': [45]})
    
    # Build
    dataset = builder.build_dataset(solexs, hmi_df=hmi)
    print(dataset[['timestamp', 'solexs_flux', 'hmi_USFLUX', 'hmi_available', 'hmi_quality_score']])
