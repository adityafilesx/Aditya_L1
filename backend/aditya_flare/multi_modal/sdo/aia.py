import numpy as np
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger("AdityaL1.MultiModal.SDO.AIA")

class AIAExtractor:
    """
    Module 3: SDO AIA Integration.
    Responsible for ingesting and processing AIA EUV images across 
    multiple wavelengths (94Å, 131Å, 171Å, 193Å, 211Å).
    Extracts high-level features such as Coronal Loop Brightness, Heating, and Active Region intensity.
    """
    def __init__(self, data_dir="data/multi_modal/sdo/aia"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.wavelengths = ['94', '131', '171', '193', '211']
        self.feature_store_path = self.data_dir / "aia_extracted_features.parquet"

    def fetch_aia_data(self, active_region_num):
        """
        Simulate fetching AIA cutouts for a specific Active Region.
        In reality, this uses sunpy Fido to download fits files.
        """
        logger.info(f"Fetching AIA image sequences for AR {active_region_num}...")
        
        # Simulate time sequence
        timestamps = pd.date_range(end=pd.Timestamp.utcnow(), periods=24, freq='1H')
        
        # Simulate extracted spatial intensity statistics
        data = {'timestamp': timestamps}
        
        for w in self.wavelengths:
            # Simulated mean intensity
            data[f'aia_{w}_mean'] = np.random.uniform(50, 500, 24)
            # Simulated max intensity (proxy for compact brightening)
            data[f'aia_{w}_max'] = data[f'aia_{w}_mean'] * np.random.uniform(2, 10, 24)
            # Simulated spatial variance (proxy for structural complexity)
            data[f'aia_{w}_var'] = np.random.uniform(100, 1000, 24)
            
        df = pd.DataFrame(data)
        return df

    def extract_physics_features(self, aia_df):
        """
        Extract physical properties from the multi-wavelength EUV combinations.
        """
        logger.info("Extracting Coronal physics features from AIA EUV...")
        df = aia_df.copy()
        
        # 1. Hot Plasma Emission Measure Proxy (uses 94A and 131A, which see ~6-10 MK plasma)
        df['hot_plasma_em_proxy'] = (df['aia_94_mean'] + df['aia_131_mean']) / 2.0
        
        # 2. Coronal Heating Proxy (Ratio of hot to warm plasma)
        # 94A (hot) vs 171A (warm ~1 MK)
        df['heating_proxy'] = df['aia_94_mean'] / (df['aia_171_mean'] + 1e-5)
        
        # 3. Loop Brightness & Activation
        # 171A, 193A, 211A track extended coronal structures and loops
        df['loop_activation_index'] = (df['aia_171_max'] + df['aia_193_max'] + df['aia_211_max']) / 3.0
        
        # 4. Structural Complexity Change (Temporal derivative of variance)
        # Sudden changes in structure often precede eruptions
        df['structural_complexity_change'] = df[['aia_131_var', 'aia_171_var', 'aia_193_var']].mean(axis=1).diff().abs()
        
        # Fill diff NaNs
        df = df.bfill()
        
        return df

    def update_feature_store(self, ar_num):
        """
        Pipeline to fetch, extract, and store AIA features.
        """
        raw_df = self.fetch_aia_data(ar_num)
        derived_df = self.extract_physics_features(raw_df)
        derived_df['active_region'] = ar_num
        
        if self.feature_store_path.exists():
            store = pd.read_parquet(self.feature_store_path)
            store = pd.concat([store, derived_df]).drop_duplicates(subset=['timestamp', 'active_region'], keep='last')
        else:
            store = derived_df
            
        store.to_parquet(self.feature_store_path)
        logger.info(f"AIA Feature Store updated. Total ARs: {store['active_region'].nunique()}")
        return store

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    aia = AIAExtractor()
    features = aia.update_feature_store(13354)
    print("AIA Derived Features Sample:", features[['timestamp', 'hot_plasma_em_proxy', 'heating_proxy', 'loop_activation_index']].head(3))
