import json

class ActiveRegionTracker:
    def __init__(self):
        self.regions = {}

    def update(self, ar_num, flux, shear):
        self.regions[ar_num] = {'flux': flux, 'shear': shear}

class EventHistory:
    def __init__(self):
        self.history = [
            {"id": "AR12673", "magnetic_flux": 3e22, "shear": 45, "outcome": "X9.3"},
            {"id": "AR11520", "magnetic_flux": 1.5e22, "shear": 30, "outcome": "X1.4"}
        ]
    
    def get_history(self):
        return self.history

class SimilarityEngine:
    def __init__(self, history):
        self.history = history

    def find_most_similar(self, current_flux, current_shear):
        def distance(hist):
            f_dist = (current_flux - hist['magnetic_flux']) / 1e22
            s_dist = (current_shear - hist['shear']) / 10.0
            return (f_dist**2 + s_dist**2)**0.5
        
        return min(self.history.get_history(), key=distance)

class SolarState:
    """
    Phase 5C: Digital Twin Refactored.
    Combines ActiveRegionTracker, EventHistory, and SimilarityEngine.
    """
    def __init__(self):
        self.ar_tracker = ActiveRegionTracker()
        self.history = EventHistory()
        self.similarity = SimilarityEngine(self.history)
        self.background_flux = 1e-8

    def ingest_telemetry(self, ar_num, flux, shear):
        self.ar_tracker.update(ar_num, flux, shear)
        
    def get_state_summary(self, ar_num):
        ar_state = self.ar_tracker.regions.get(ar_num, {})
        if not ar_state:
            return None
            
        sim = self.similarity.find_most_similar(ar_state['flux'], ar_state['shear'])
        
        return {
            "active_region": ar_num,
            "current_state": ar_state,
            "similar_historical_event": sim
        }

if __name__ == "__main__":
    state = SolarState()
    state.ingest_telemetry(13354, 2e22, 35)
    print(json.dumps(state.get_state_summary(13354), indent=2))
