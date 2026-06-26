import numpy as np
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger("AdityaL1.MultiModal.SWIS")

class SolarWindExtractor:
    """
    Module 4: SWIS Integration (Solar Wind Ion Spectrometer).
    Responsible for fetching in-situ solar wind plasma parameters.
    Extracts Velocity, Density, Temperature, and Alpha Ratio, primarily used 
    for predicting Space Environment impacts (SEP, Geomagnetic storms).
    """
    def __init__(self, data_dir="data/multi_modal/swis"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.feature_store_path = self.data_dir / "swis_features.parquet"

    def fetch_swis_data(self):
        """
        Simulate fetching continuous solar wind telemetry from Aditya-L1 SWIS
        or DSCOVR/ACE L1 monitors.
        """
        logger.info("Fetching Solar Wind telemetry...")
        
        # Simulated continuous data stream
        timestamps = pd.date_range(end=pd.Timestamp.utcnow(), periods=24, freq='1H')
        
        # Raw SWIS parameters
        df = pd.DataFrame({
            'timestamp': timestamps,
            'sw_velocity': np.random.uniform(300, 800, 24),     # km/s (typical 400, fast >600)
            'sw_density': np.random.uniform(1, 20, 24),         # protons/cm^3
            'sw_temperature': np.random.uniform(1e4, 1e6, 24),  # Kelvin
            'sw_alpha_ratio': np.random.uniform(0.01, 0.08, 24) # He++ / H+ ratio (CME indicator if > 0.08)
        })
        return df

    def compute_space_weather_indices(self, swis_df):
        """
        Compute higher-order indices relevant for Earth-impact predictions.
        """
        logger.info("Computing Space Weather impact indices from solar wind...")
        df = swis_df.copy()
        
        # 1. Dynamic Pressure (P = proton_mass * density * velocity^2)
        # Simplified proxy proportional to n * v^2
        df['dynamic_pressure_proxy'] = df['sw_density'] * (df['sw_velocity'] ** 2) * 1e-6
        
        # 2. Fast Wind Indicator (Boolean proxy for Coronal Hole High Speed Streams)
        df['is_high_speed_stream'] = (df['sw_velocity'] > 500).astype(int)
        
        # 3. CME Arrival Signature Proxy
        # ICMEs often show low temperature and enhanced alpha ratio
        df['cme_signature_score'] = df['sw_alpha_ratio'] * (1e5 / (df['sw_temperature'] + 1))
        
        # 4. Stream Interaction Region (SIR) Proxy
        # Density pile-up followed by velocity increase
        df['density_gradient'] = df['sw_density'].diff()
        df['velocity_gradient'] = df['sw_velocity'].diff()
        # SIRs happen when positive density gradient is followed/coincides with positive velocity gradient
        df['sir_proxy'] = df['density_gradient'].clip(lower=0) * df['velocity_gradient'].clip(lower=0)
        
        df = df.bfill()
        
        return df

    def update_feature_store(self):
        """
        Pipeline to fetch, compute, and store SWIS features.
        """
        raw_df = self.fetch_swis_data()
        derived_df = self.compute_space_weather_indices(raw_df)
        
        if self.feature_store_path.exists():
            store = pd.read_parquet(self.feature_store_path)
            store = pd.concat([store, derived_df]).drop_duplicates(subset=['timestamp'], keep='last')
        else:
            store = derived_df
            
        store.to_parquet(self.feature_store_path)
        logger.info(f"SWIS Feature Store updated. Total records: {len(store)}")
        return store

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    swis = SolarWindExtractor()
    features = swis.update_feature_store()
    print("SWIS Derived Features Sample:", features[['timestamp', 'sw_velocity', 'dynamic_pressure_proxy', 'cme_signature_score']].head(3))
