import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)
router = APIRouter()

class MLConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"ML WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"ML WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting to WS: {e}")

manager = MLConnectionManager()

async def broadcast_periodic_monitoring():
    """Simulates broadcasting live monitoring metrics, training progress, and experiment updates."""
    from backend.ml.registry.model_registry import model_registry
    from backend.ml.training.training_manager import training_manager
    
    while True:
        try:
            # Gather training job progress
            job_progress = {}
            if training_manager.active_training_jobs:
                # Get the latest job
                latest_job_id = list(training_manager.active_training_jobs.keys())[-1]
                job_progress = training_manager.active_training_jobs[latest_job_id]
            
            payload = {
                "type": "ML_MONITORING_UPDATE",
                "payload": {
                    "latency_ms": 3.8,
                    "memory_usage_pct": 42.1,
                    "cpu_usage_pct": 18.5,
                    "gpu_usage_pct": 0.0,
                    "calibration_drift": 0.012,
                    "feature_drift": 0.045,
                    "prediction_drift": 0.021,
                    "data_drift": 0.018,
                    "status": "NOMINAL",
                    "job_progress": job_progress,
                    "active_model": model_registry.get_active_model().dict() if model_registry.get_active_model() else None
                }
            }
            await manager.broadcast(payload)
        except Exception as e:
            logger.error(f"Periodic WS broadcast error: {e}")
        await asyncio.sleep(5)

@router.on_event("startup")
async def startup_event():
    asyncio.create_task(broadcast_periodic_monitoring())

@router.websocket("/ml")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Client can send commands
            data = await websocket.receive_text()
            logger.info(f"Received ML WS client message: {data}")
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)
