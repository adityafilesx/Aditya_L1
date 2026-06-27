import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8000/ws/live"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to", uri)
            msg = await websocket.recv()
            print(json.dumps(json.loads(msg), indent=2))
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test_ws())
