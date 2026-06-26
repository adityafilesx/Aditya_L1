import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from events.mission_bus import mission_bus
from events.generator import generator

logger = logging.getLogger(__name__)
router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")

manager = ConnectionManager()

async def forward_channel_to_websocket(channel: str, websocket: WebSocket):
    queue = mission_bus.subscribe(channel)
    try:
        while True:
            # Wait for next message on this channel
            message = await queue.get()
            payload = {
                "type": channel.upper(),
                "payload": message
            }
            await websocket.send_text(json.dumps(payload))
            queue.task_done()
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.error(f"Error forwarding channel {channel}: {e}")
    finally:
        mission_bus.unsubscribe(channel, queue)

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    # We will subscribe to all major channels to satisfy the real-time requirements
    channels = [
        "mission_state", "telemetry", "forecast", "physics", 
        "digital_twin", "system", "alerts"
    ]
    
    tasks = []
    try:
        # Create a forwarding task for each channel
        for channel in channels:
            task = asyncio.create_task(forward_channel_to_websocket(channel, websocket))
            tasks.append(task)
            
        # Keep connection open until client disconnects
        while True:
            # Client can send commands (e.g. for replay engine)
            data = await websocket.receive_text()
            try:
                command = json.loads(data)
                # Handle commands like {"action": "pause"}, {"action": "set_speed", "value": 2}
                logger.info(f"Received WS command: {command}")
            except json.JSONDecodeError:
                pass
                
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)
        for task in tasks:
            task.cancel()
