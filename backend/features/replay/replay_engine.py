from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from backend.features.models import ScientificFeatureVector
from backend.features.repository.feature_store import feature_store

class FeatureReplayEngine:
    """Replays historical feature vectors for training runs, validation, or simulations."""

    def get_replay_dataset(
        self,
        time_window: Optional[str] = None,  # "hour", "day"
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        master_id: Optional[str] = None
    ) -> List[ScientificFeatureVector]:
        all_vectors = feature_store.get_all()
        
        if master_id:
            # Replay by a single master event
            vec = feature_store.get_by_master_id(master_id)
            return [vec] if vec else []

        now = datetime.utcnow()
        if time_window == "hour":
            s_dt = now - timedelta(hours=1)
        elif time_window == "day":
            s_dt = now - timedelta(days=1)
        else:
            s_dt = None

        results = []
        for vec in all_vectors:
            try:
                vec_dt = datetime.fromisoformat(vec.provenance.extracted_at.replace("Z", "+00:00")).replace(tzinfo=None)
                if s_dt and vec_dt < s_dt:
                    continue
                if start_time:
                    st = datetime.fromisoformat(start_time.replace("Z", "+00:00")).replace(tzinfo=None)
                    if vec_dt < st:
                        continue
                if end_time:
                    et = datetime.fromisoformat(end_time.replace("Z", "+00:00")).replace(tzinfo=None)
                    if vec_dt > et:
                        continue
            except:
                pass
            results.append(vec)

        return results


# Global singleton instance
replay_engine = FeatureReplayEngine()
