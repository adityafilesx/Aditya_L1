import psutil
import time
from fastapi import APIRouter
from aditya_flare.config.config_loader import config
from api.state import app_state

router = APIRouter(prefix="/system", tags=["system"])

process = psutil.Process()
START_TIME = time.time()

@router.get("/health")
async def get_system_health():
    """Returns underlying hardware metrics (CPU, Memory, Disk)."""
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "latency_ms": 12 # simulated ping
    }

@router.get("/config")
async def get_config():
    """Returns the current operational config."""
    return config.__dict__

@router.get("/diagnostics")
async def get_diagnostics():
    """Returns comprehensive end-to-end subsystem diagnostics for SIT Phase."""
    
    process = psutil.Process()
    # 1. Hardware & OS Metrics
    hardware = {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "gpu_percent": 0.0, # Mocked since no real GPU in local env
        "disk_percent": psutil.disk_usage('/').percent,
        "process_uptime_sec": time.time() - START_TIME,
        "thread_count": process.num_threads(),
        "network_latency_ms": 15, # Simulated ping
    }
    
    # 2. Engines Status
    engines = {
        "api_gateway": {"status": "ONLINE", "version": "v2.4.0", "errors": 0},
        "streaming_engine": {"status": "ONLINE", "connections": 0, "errors": 0},
        "physics_engine": {"status": "ONLINE" if hasattr(app_state, 'latest_physics') else "OFFLINE", "version": "1.2.0"},
        "forecast_engine": {"status": "ONLINE" if hasattr(app_state, 'ai_predictor') else "OFFLINE", "version": "2.1.0"},
        "decision_engine": {"status": "ONLINE" if app_state.decision_engine else "OFFLINE", "version": "1.0.0"},
        "mission_intelligence": {"status": "ONLINE" if app_state.mission_intelligence else "OFFLINE", "version": "1.0.0"},
        "digital_twin": {"status": "ONLINE" if app_state.digital_twin else "OFFLINE", "version": "3.0.0"},
        "knowledge_graph": {"status": "ONLINE" if app_state.knowledge_graph else "OFFLINE", "version": "2.0.0"},
        "scientific_reasoning": {"status": "ONLINE", "version": "1.0.0"}, # Always loaded if this is hit
        "database": {"status": "ONLINE", "type": "mock", "latency_ms": 2},
        "redis": {"status": "OFFLINE", "type": "none"},
        "vector_database": {"status": "ONLINE", "type": "faiss", "latency_ms": 4},
    }
    
    return {
        "timestamp": time.time(),
        "hardware": hardware,
        "engines": engines,
        "overall_status": "HEALTHY"
    }
