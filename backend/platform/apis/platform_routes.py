from fastapi import APIRouter
from typing import Dict, Any
from backend.platform.monitoring.health import system_health_manager
from backend.platform.diagnostics.engine import diagnostics_engine
from backend.platform.benchmarking.manager import benchmark_manager
from backend.platform.recovery.manager import recovery_manager

router = APIRouter(prefix="/api/platform", tags=["platform"])

@router.get("/health")
def get_health():
    return system_health_manager.get_system_health()

@router.get("/diagnostics")
def run_diag():
    return diagnostics_engine.run_diagnostics()

@router.get("/benchmarks")
def get_bench():
    return benchmark_manager.get_latencies_ms()

@router.post("/inject-failure")
def inject_fail(subsystem: str):
    system_health_manager.inject_failure(subsystem)
    return {"status": f"Injected failure in: {subsystem}"}

@router.post("/recover")
def recover_sub(subsystem: str):
    return recovery_manager.trigger_recovery(subsystem)
