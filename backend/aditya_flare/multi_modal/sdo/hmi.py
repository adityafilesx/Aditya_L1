import pandas as pd
import numpy as np
import logging
from pathlib import Path

logger = logging.getLogger("AdityaL1.MultiModal.SDO.HMI")

class HMIExtractor:
    """
    Module 2: SDO HMI Integration.
    Responsible for fetching SHARP (Space-weather HMI Active Region Patches) 
    parameters and computing higher-order magnetic properties.
    """
    def __init__(self, data_dir="data/multi_modal/sdo/hmi"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.feature_store_path = self.data_dir / "hmi_sharp_features.parquet"

    def fetch_sharp_parameters(self, active_region_num):
        """
        Simulate downloading SHARP parameters from JSOC via drms.
        Returns a time-series of magnetic properties for the given AR.
        """
        logger.info(f"Fetching SHARP parameters for AR {active_region_num}...")
        
        # Simulated JSOC response (normally downloaded via sunpy/drms)
        timestamps = pd.date_range(end=pd.Timestamp.utcnow(), periods=24, freq='1H')
        
        # Raw SHARP parameters
        df = pd.DataFrame({
            'timestamp': timestamps,
            'hmi_USFLUX': np.random.uniform(1e21, 5e22, 24),    # Total unsigned flux
            'hmi_ERRVFAS': np.random.uniform(0.01, 0.1, 24),    # Error
            'hmi_MEANJZH': np.random.uniform(-0.05, 0.05, 24),  # Mean current helicity
            'hmi_TOTUSJH': np.random.uniform(100, 1000, 24),    # Total unsigned current helicity
            'hmi_ABSNJZH': np.random.uniform(10, 500, 24),      # Absolute net current helicity
            'hmi_SAVNCPP': np.random.uniform(1e12, 1e13, 24),   # Sum of net current per polarity
            'hmi_MEANPOT': np.random.uniform(5000, 15000, 24),  # Mean photospheric magnetic free energy
            'hmi_MEANSHR': np.random.uniform(10, 45, 24),       # Mean shear angle
            'hmi_R_VALUE': np.random.uniform(2.0, 5.5, 24)      # Schrijver R value (flux near neutral line)
        })
        return df

    def compute_derived_features(self, sharp_df):
        """
        Compute higher-order magnetic properties from the base SHARP parameters.
        Includes Gradient, Shear changes, Free Energy proxies, and Neutral Line dynamics.
        """
        logger.info("Computing derived HMI magnetic features...")
        df = sharp_df.copy()
        
        # 1. Flux Emergence Rate (Derivative of USFLUX over time)
        df['hmi_flux_emergence_rate'] = df['hmi_USFLUX'].diff() / 3600.0  # flux per second
        
        # 2. Helicity Injection Proxy
        # Simulated proxy combining total unsigned current helicity and flux changes
        df['hmi_helicity_injection'] = df['hmi_TOTUSJH'] * np.abs(df['hmi_flux_emergence_rate'])
        
        # 3. Shear Gradient
        df['hmi_shear_gradient'] = df['hmi_MEANSHR'].diff()
        
        # 4. Non-potentiality Index (Free Energy proxy)
        # Using MEANPOT normalized by Total Unsigned Flux
        df['hmi_non_potentiality'] = df['hmi_MEANPOT'] / (df['hmi_USFLUX'] + 1e-10)
        
        # 5. Neutral Line Activity Proxy
        # Combining R_VALUE and absolute net current helicity
        df['hmi_neutral_line_activity'] = df['hmi_R_VALUE'] * np.log1p(df['hmi_ABSNJZH'])
        
        # Fill first row NaNs from diff()
        df = df.bfill()
        
        return df

    def update_feature_store(self, ar_num):
        """
        End-to-end pipeline to fetch, compute, and store HMI features.
        """
        sharp_df = self.fetch_sharp_parameters(ar_num)
        derived_df = self.compute_derived_features(sharp_df)
        derived_df['active_region'] = ar_num
        
        if self.feature_store_path.exists():
            store = pd.read_parquet(self.feature_store_path)
            # Append and deduplicate
            store = pd.concat([store, derived_df]).drop_duplicates(subset=['timestamp', 'active_region'], keep='last')
        else:
            store = derived_df
            
        store.to_parquet(self.feature_store_path)
        logger.info(f"HMI Feature Store updated. Total ARs: {store['active_region'].nunique()}")
        return store

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    hmi = HMIExtractor()
    features = hmi.update_feature_store(13354)
    print("HMI Derived Features Sample:", features[['timestamp', 'hmi_flux_emergence_rate', 'hmi_non_potentiality', 'hmi_neutral_line_activity']].head(3))
