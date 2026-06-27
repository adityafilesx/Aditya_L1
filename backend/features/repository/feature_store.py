from typing import Dict, List, Optional
from backend.features.models import ScientificFeatureVector

class FeatureStore:
    """In-memory storage for ScientificFeatureVectors.

    Serves as the feature store for downstream ML algorithms, maintaining
    quick retrieval indexes and exporting options for tabular data.
    """

    def __init__(self):
        self._store: Dict[str, ScientificFeatureVector] = {}
        self._physics_index: Dict[str, str] = {}
        self._master_index: Dict[str, str] = {}

    def store(self, feature_vector: ScientificFeatureVector) -> None:
        """Store a feature vector and update search indexes."""
        fid = feature_vector.feature_vector_id
        self._store[fid] = feature_vector
        
        if feature_vector.physics_product_id:
            self._physics_index[feature_vector.physics_product_id] = fid
        if feature_vector.master_id:
            self._master_index[feature_vector.master_id] = fid

    def get_by_id(self, feature_vector_id: str) -> Optional[ScientificFeatureVector]:
        """Retrieve feature vector by its unique ID."""
        return self._store.get(feature_vector_id)

    def get_by_physics_id(self, physics_product_id: str) -> Optional[ScientificFeatureVector]:
        """Retrieve feature vector linked to a physics product ID."""
        fid = self._physics_index.get(physics_product_id)
        if fid:
            return self.get_by_id(fid)
        return None

    def get_by_master_id(self, master_id: str) -> Optional[ScientificFeatureVector]:
        """Retrieve feature vector linked to a Master catalog entry ID."""
        fid = self._master_index.get(master_id)
        if fid:
            return self.get_by_id(fid)
        return None

    def get_all(self) -> List[ScientificFeatureVector]:
        """Retrieve all stored feature vectors."""
        return list(self._store.values())

    def get_flat_matrix(self) -> List[List[float]]:
        """Return all features as a matrix (list of lists of floats) sorted by ID."""
        sorted_keys = sorted(self._store.keys())
        return [self._store[k].to_flat_list() for k in sorted_keys]

    def clear(self) -> None:
        """Clear the store and indexes."""
        self._store.clear()
        self._physics_index.clear()
        self._master_index.clear()


# Global singleton instance
feature_store = FeatureStore()
