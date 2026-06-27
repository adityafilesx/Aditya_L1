"""
REST API endpoints for the Physics Characterization Engine.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict

from backend.physics.repository.physics_repository import physics_repository
from backend.physics.models import PhysicsCharacterization

router = APIRouter(prefix="/physics", tags=["physics"])


@router.get("/product/{physics_product_id}", response_model=PhysicsCharacterization)
async def get_physics_product(physics_product_id: str):
    """Fetch full physics product by ID."""
    product = physics_repository.get_by_id(physics_product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Physics product not found")
    return product


@router.get("/by-catalog/{master_id}", response_model=PhysicsCharacterization)
async def get_physics_by_catalog(master_id: str):
    """Resolve physics product from catalog ID."""
    product = physics_repository.get_by_master_id(master_id)
    if not product:
        raise HTTPException(status_code=404, detail="Physics product not found for this master_id")
    return product


@router.get("/state")
async def get_physics_state():
    """Current physics state (latest product)."""
    latest = physics_repository.get_latest(1)
    if not latest:
        return {}
    return latest[0]


@router.get("/thermal/{physics_product_id}")
async def get_thermal_profile(physics_product_id: str):
    product = physics_repository.get_by_id(physics_product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.thermal


@router.get("/spectral/{physics_product_id}")
async def get_spectral_profile(physics_product_id: str):
    product = physics_repository.get_by_id(physics_product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.spectral


@router.get("/neupert/{physics_product_id}")
async def get_neupert_profile(physics_product_id: str):
    product = physics_repository.get_by_id(physics_product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.neupert


@router.get("/classification/{physics_product_id}")
async def get_classification(physics_product_id: str):
    product = physics_repository.get_by_id(physics_product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.classification


@router.get("/indices/{physics_product_id}")
async def get_indices(physics_product_id: str):
    product = physics_repository.get_by_id(physics_product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.indices


@router.get("/quality/{physics_product_id}")
async def get_quality(physics_product_id: str):
    product = physics_repository.get_by_id(physics_product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.quality


@router.get("/repository/history", response_model=List[PhysicsCharacterization])
async def get_history(limit: int = 50):
    """Physics history."""
    return physics_repository.get_history(limit)


@router.get("/repository/statistics")
async def get_statistics() -> Dict:
    """Aggregate physics stats."""
    return physics_repository.get_statistics()


@router.get("/repository/export")
async def get_export():
    """JSON export."""
    from fastapi.responses import Response
    json_data = physics_repository.export_json()
    return Response(content=json_data, media_type="application/json")


@router.get("/detector/benchmark")
async def get_detector_benchmarks():
    """Detector benchmarks."""
    from backend.nowcasting.manager import nowcast_manager
    return {
        "solexs": nowcast_manager.solexs_benchmark.get_snapshot(),
        "helios": nowcast_manager.helios_benchmark.get_snapshot(),
    }
