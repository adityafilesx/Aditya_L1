import numpy as np
import pandas as pd
import json
import logging
from datetime import datetime

logger = logging.getLogger("AdityaL1.MultiModal.DigitalTwin")

class SolarDigitalTwin:
    """
    Module 7: Solar Digital Twin.
    Maintains a live state representation of the Sun, tracking Active Regions,
    their history, evolution, and generating similarities to historical events.
    """
    def __init__(self):
        self.active_regions = {}
        self.global_state = {
            "last_updated": None,
            "xrs_background": None,
            "proton_flux": None,
            "kp_index_proxy": None
        }
        # A mocked historical database of AR states and their flare outcomes
        self.historical_db = [
            {"id": "AR12673", "magnetic_flux": 3e22, "shear": 45, "outcome": "X9.3"},
            {"id": "AR11520", "magnetic_flux": 1.5e22, "shear": 30, "outcome": "X1.4"},
            {"id": "AR13354", "magnetic_flux": 5e21, "shear": 15, "outcome": "M1.2"}
        ]

    def update_global_state(self, telemetry, swis):
        """
        Update the full-disk background state using GOES and SWIS.
        """
        self.global_state['last_updated'] = datetime.utcnow().isoformat()
        # Simulated extraction from the latest row
        self.global_state['xrs_background'] = telemetry['goes_xrs_b'].iloc[-1]
        self.global_state['proton_flux'] = swis['sw_density'].iloc[-1] # proxy
        
        logger.info(f"Global Solar State updated at {self.global_state['last_updated']}")

    def track_active_region(self, ar_num, hmi_features, aia_features):
        """
        Update the tracked state of a specific Active Region.
        """
        # Get the latest features
        latest_hmi = hmi_features.iloc[-1]
        latest_aia = aia_features.iloc[-1]
        
        state = {
            "updated_at": datetime.utcnow().isoformat(),
            "magnetic_flux": latest_hmi.get('USFLUX', 0),
            "shear": latest_hmi.get('MEANSHR', 0),
            "non_potentiality": latest_hmi.get('non_potentiality', 0),
            "heating_proxy": latest_aia.get('heating_proxy', 0)
        }
        
        self.active_regions[ar_num] = state
        logger.info(f"Active Region {ar_num} state updated in Digital Twin.")
        
    def find_historical_similarity(self, ar_num):
        """
        Computes Euclidean distance between the current AR state and the historical DB 
        to find the most similar past event.
        """
        if ar_num not in self.active_regions:
            return None
            
        current_state = self.active_regions[ar_num]
        
        # Simple similarity based on Flux and Shear
        def distance(hist):
            f_dist = (current_state['magnetic_flux'] - hist['magnetic_flux']) / 1e22
            s_dist = (current_state['shear'] - hist['shear']) / 10.0
            return np.sqrt(f_dist**2 + s_dist**2)
            
        best_match = min(self.historical_db, key=distance)
        
        return {
            "similar_region": best_match['id'],
            "historical_outcome": best_match['outcome'],
            "distance_score": distance(best_match)
        }
        
    def get_full_state(self):
        """
        Return JSON representation of the entire Solar Digital Twin.
        """
        return json.dumps({
            "global_state": self.global_state,
            "active_regions": self.active_regions
        }, indent=2)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    twin = SolarDigitalTwin()
    
    # Mock some data
    mock_telemetry = pd.DataFrame({'goes_xrs_b': [1e-6]})
    mock_swis = pd.DataFrame({'sw_density': [5.0]})
    mock_hmi = pd.DataFrame({'USFLUX': [2e22], 'MEANSHR': [40], 'non_potentiality': [0.5]})
    mock_aia = pd.DataFrame({'heating_proxy': [1.2]})
    
    twin.update_global_state(mock_telemetry, mock_swis)
    twin.track_active_region(14000, mock_hmi, mock_aia)
    
    similarity = twin.find_historical_similarity(14000)
    print("Most similar historical event:", similarity)
    
    print("\nFull Twin State:")
    print(twin.get_full_state())
