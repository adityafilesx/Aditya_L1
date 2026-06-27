import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from backend.observation_engine.observation_manager import observation_manager
from backend.api.mock_data import generate_mock_telemetry  # using existing mock raw telemetry as input

router = APIRouter()

class ObservationConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._task = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # Start broadcast loop if not running
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._broadcast_loop())

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        if not self.active_connections and self._task:
            self._task.cancel()
            self._task = None

    async def _broadcast_loop(self):
        try:
            while self.active_connections:
                # 1. Get raw telemetry (from existing mock source to simulate instrument data)
                raw_data = generate_mock_telemetry()
                
                # 2. Process through Observation Manager
                obs = observation_manager.process_raw_telemetry(raw_data)
                
                # 3. Broadcast enriched payload
                payload = {
                    "type": "observation",
                    "data": obs.dict()
                }
                
                # Also send pipeline status
                status_payload = {
                    "type": "pipeline_status",
                    "data": {
                        "status": "GREEN" if obs.quality.overall_scientific_confidence >= 0.8 else "YELLOW",
                        "observation_rate_hz": 1.0,
                        "current_latency_ms": obs.provenance.total_latency_ms,
                        "active_instruments": ["SoLEXS", "HEL1OS"],
                        "system_health": "NOMINAL",
                        "last_updated": obs.timestamp
                    }
                }
                
                # Clean up disconnected clients during broadcast
                disconnected = []
                for connection in self.active_connections:
                    try:
                        await connection.send_text(json.dumps(payload, default=str))
                        await connection.send_text(json.dumps(status_payload, default=str))
                    except Exception:
                        disconnected.append(connection)
                        
                for conn in disconnected:
                    self.active_connections.remove(conn)
                    
                await asyncio.sleep(1.0)  # Stream at 1Hz
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Observation broadcast error: {e}")

manager = ObservationConnectionManager()

@router.websocket("/stream")
async def observation_stream(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection open, wait for client messages if any
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
