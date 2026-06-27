"""
WebSocket endpoint for the Scientific Nowcasting Engine.

Streams ``NowcastState`` at 1Hz to all connected clients.
The nowcast manager is fed by the observation stream, and its output
is broadcast alongside observation data.
"""

import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime, timezone

from backend.nowcasting.manager import nowcast_manager

router = APIRouter()


class NowcastConnectionManager:
    """Manages WebSocket connections for nowcasting stream."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._task = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._broadcast_loop())

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if not self.active_connections and self._task:
            self._task.cancel()
            self._task = None

    async def _broadcast_loop(self):
        try:
            while self.active_connections:
                timestamp = datetime.now(timezone.utc).isoformat()
                obs_quality = 0.9  # default quality

                # Process one tick through the nowcast engine
                state = nowcast_manager.process_observation(
                    solexs_flux=0,   # these are overridden by the simulator inside the manager
                    helios_flux=0,
                    timestamp=timestamp,
                    obs_quality=obs_quality,
                )

                payload = {
                    "type": "nowcast_state",
                    "data": state.dict(),
                }

                disconnected = []
                for conn in self.active_connections:
                    try:
                        await conn.send_text(json.dumps(payload, default=str))
                    except Exception:
                        disconnected.append(conn)

                for conn in disconnected:
                    if conn in self.active_connections:
                        self.active_connections.remove(conn)

                await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Nowcast broadcast error: {e}")


nc_manager = NowcastConnectionManager()


@router.websocket("/stream")
async def nowcast_stream(websocket: WebSocket):
    await nc_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        nc_manager.disconnect(websocket)
