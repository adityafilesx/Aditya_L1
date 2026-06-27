from typing import Dict, List, Any
from pydantic import BaseModel

class LineageNode(BaseModel):
    node_id: str
    type: str  # "Observation", "Nowcast", "Physics", "Validation", "Normalization", "FeatureVector"
    version: str
    timestamp: str
    status: str
    metadata: Dict[str, Any] = {}


class FeatureLineageEngine:
    """Tracks complete end-to-end scientific lineage for feature vectors."""

    def __init__(self):
        # Maps feature_vector_id to list of LineageNodes
        self._lineage_store: Dict[str, List[LineageNode]] = {}

    def record_lineage(
        self,
        feature_vector_id: str,
        master_id: str,
        physics_product_id: str,
        observation_ids: List[str],
        validation_status: str,
        normalization_version: str,
        timestamp_str: str
    ) -> None:
        nodes = []

        # 1. Observation Nodes
        for obs_id in observation_ids:
            nodes.append(LineageNode(
                node_id=obs_id,
                type="Observation",
                version="1.0.0",
                timestamp=timestamp_str,
                status="VALIDATED",
                metadata={}
            ))

        # 2. Nowcasting Node
        nodes.append(LineageNode(
            node_id=master_id,
            type="Nowcast",
            version="1.0.0",
            timestamp=timestamp_str,
            status="CONFIRMED",
            metadata={}
        ))

        # 3. Physics Node
        nodes.append(LineageNode(
            node_id=physics_product_id,
            type="Physics",
            version="1.0.0",
            timestamp=timestamp_str,
            status="COMPLETED",
            metadata={}
        ))

        # 4. Feature Vector Node
        nodes.append(LineageNode(
            node_id=feature_vector_id,
            type="FeatureVector",
            version="1.0.0",
            timestamp=timestamp_str,
            status="ML_READY" if validation_status == "VALID" else "DEGRADED",
            metadata={
                "validation_status": validation_status,
                "normalization_version": normalization_version
            }
        ))

        self._lineage_store[feature_vector_id] = nodes

    def get_lineage(self, feature_vector_id: str) -> List[LineageNode]:
        return self._lineage_store.get(feature_vector_id, [])


# Global singleton instance
lineage_engine = FeatureLineageEngine()
