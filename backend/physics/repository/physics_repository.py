"""
Physics Repository.

In-memory storage for PhysicsCharacterization products.
Generates unique Physics Product IDs (PHY-YYYYMMDD-NNN).
Supports lookups by physics_product_id or master_id (back-reference).
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional, Dict
from datetime import datetime
import json

from backend.physics.models import PhysicsCharacterization


class PhysicsRepository:
    """In-memory repository for fully characterized physics products."""

    def __init__(self, max_size: int = 500):
        self._products: deque[PhysicsCharacterization] = deque(maxlen=max_size)
        self._counter: int = 0
        self._date_prefix: str = datetime.utcnow().strftime('%Y%m%d')

    def _generate_id(self) -> str:
        """Generate a unique Physics Product ID (PHY-YYYYMMDD-NNN)."""
        now_date = datetime.utcnow().strftime('%Y%m%d')
        if now_date != self._date_prefix:
            self._date_prefix = now_date
            self._counter = 0
            
        self._counter += 1
        return f"PHY-{self._date_prefix}-{self._counter:03d}"

    def store(self, product: PhysicsCharacterization) -> str:
        """Assign ID and store product. Returns the generated ID."""
        if not product.physics_product_id:
            product.physics_product_id = self._generate_id()
        self._products.append(product)
        return product.physics_product_id

    def get_by_id(self, physics_product_id: str) -> Optional[PhysicsCharacterization]:
        """Lookup by the unique physics product ID."""
        for p in self._products:
            if p.physics_product_id == physics_product_id:
                return p
        return None

    def get_by_master_id(self, master_id: str) -> Optional[PhysicsCharacterization]:
        """Lookup by the associated Master Flare Catalog ID."""
        for p in self._products:
            if p.master_id == master_id:
                return p
        return None

    def get_latest(self, n: int = 1) -> List[PhysicsCharacterization]:
        return list(self._products)[-n:]

    def get_history(self, limit: int = 50) -> List[PhysicsCharacterization]:
        return list(reversed(list(self._products)[-limit:]))

    def search(self, query: str) -> List[PhysicsCharacterization]:
        q = query.lower()
        return [
            p for p in self._products
            if q in p.physics_product_id.lower() or q in p.master_id.lower()
        ]

    def get_statistics(self) -> Dict:
        total = len(self._products)
        if total == 0:
            return {"total": 0}
            
        avg_thermal_energy = sum(p.thermal.thermal_energy for p in self._products) / total
        avg_quality = sum(p.quality.overall_quality_score for p in self._products) / total
        
        return {
            "total_products": total,
            "average_thermal_energy_erg": avg_thermal_energy,
            "average_quality_score": avg_quality,
        }

    def export_json(self) -> str:
        return json.dumps([p.dict() for p in self._products], indent=2, default=str)


# Global singleton
physics_repository = PhysicsRepository()
