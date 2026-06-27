from typing import List, Optional
from collections import deque
from .models import EnrichedObservation

class ObservationRepository:
    def __init__(self, max_history=1000):
        self.history: deque = deque(maxlen=max_history)
    
    def store(self, obs: EnrichedObservation):
        self.history.append(obs)
        
    def get_latest(self) -> Optional[EnrichedObservation]:
        if not self.history:
            return None
        return self.history[-1]
        
    def get_history(self, limit: int = 100) -> List[EnrichedObservation]:
        return list(self.history)[-limit:]
        
    def search_by_id(self, obs_id: str) -> Optional[EnrichedObservation]:
        for obs in self.history:
            if obs.provenance.observation_id == obs_id:
                return obs
        return None
        
    def export(self) -> List[dict]:
        return [obs.dict() for obs in self.history]
