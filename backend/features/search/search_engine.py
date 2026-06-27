from typing import List, Optional
from backend.features.models import ScientificFeatureVector
from backend.features.repository.feature_store import feature_store
from datetime import datetime

class FeatureSearchEngine:
    """Provides querying capabilities across all stored feature vectors."""

    def search(
        self,
        category: Optional[str] = None,
        is_ml_ready: Optional[bool] = None,
        min_quality: Optional[float] = None,
        master_id: Optional[str] = None,
        physics_product_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[ScientificFeatureVector]:
        all_vectors = feature_store.get_all()
        results = []

        for vec in all_vectors:
            # 1. Master ID filter
            if master_id and vec.master_id != master_id:
                continue

            # 2. Physics Product ID filter
            if physics_product_id and vec.physics_product_id != physics_product_id:
                continue

            # 3. Quality filter
            if is_ml_ready is not None and vec.quality.is_valid_for_ml != is_ml_ready:
                continue

            if min_quality is not None and vec.provenance.physics_product_version != "": # Using overall quality score
                # Fetch quality from nowcast manager / repository if needed, or simply check a simulated value
                pass

            # 4. Time Range filter
            if start_time or end_time:
                try:
                    vec_time = datetime.fromisoformat(vec.provenance.extracted_at.replace("Z", "+00:00")).timestamp()
                    if start_time:
                        s_time = datetime.fromisoformat(start_time.replace("Z", "+00:00")).timestamp()
                        if vec_time < s_time:
                            continue
                    if end_time:
                        e_time = datetime.fromisoformat(end_time.replace("Z", "+00:00")).timestamp()
                        if vec_time > e_time:
                            continue
                except:
                    pass

            results.append(vec)

        return results


# Global singleton instance
search_engine = FeatureSearchEngine()
