import asyncio
import logging
from typing import Callable, Awaitable, List, Dict, Any

logger = logging.getLogger(__name__)

class MissionBus:
    """
    Central Pub/Sub Event Bus for real-time streaming architecture.
    """
    def __init__(self):
        # channel_name -> list of subscriber queues
        self._subscribers: Dict[str, List[asyncio.Queue]] = {}

    def subscribe(self, channel: str) -> asyncio.Queue:
        if channel not in self._subscribers:
            self._subscribers[channel] = []
        
        queue = asyncio.Queue()
        self._subscribers[channel].append(queue)
        logger.debug(f"Subscribed to channel: {channel}. Total subscribers: {len(self._subscribers[channel])}")
        return queue

    def unsubscribe(self, channel: str, queue: asyncio.Queue):
        if channel in self._subscribers and queue in self._subscribers[channel]:
            self._subscribers[channel].remove(queue)
            logger.debug(f"Unsubscribed from channel: {channel}. Remaining subscribers: {len(self._subscribers[channel])}")

    async def publish(self, channel: str, message: Any):
        if channel not in self._subscribers:
            return
            
        for queue in self._subscribers[channel]:
            try:
                # Non-blocking put, or very short wait
                queue.put_nowait(message)
            except asyncio.QueueFull:
                logger.warning(f"Queue full for channel {channel}, dropping message")
            except Exception as e:
                logger.error(f"Error publishing to {channel}: {e}")

# Global instance
mission_bus = MissionBus()
