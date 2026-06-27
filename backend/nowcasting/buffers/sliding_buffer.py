"""
Dedicated sliding observation buffers for the Nowcasting Engine.

Each detector maintains its own independent buffer so that buffer operations
(mean, sigma, derivative, rolling average) are isolated and do not interfere
with one another.
"""

from __future__ import annotations

import math
from collections import deque
from typing import List, Optional


class SlidingBuffer:
    """Fixed-size sliding window buffer with statistical helpers.

    Parameters
    ----------
    max_size : int
        Maximum number of observations retained.
    """

    def __init__(self, max_size: int = 120):
        self._max_size = max_size
        self._data: deque[float] = deque(maxlen=max_size)
        self._timestamps: deque[str] = deque(maxlen=max_size)

    # ------------------------------------------------------------------
    # Ingestion
    # ------------------------------------------------------------------

    def push(self, value: float, timestamp: str = "") -> None:
        """Append a new observation to the buffer."""
        self._data.append(value)
        self._timestamps.append(timestamp)

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    @property
    def values(self) -> List[float]:
        return list(self._data)

    @property
    def timestamps(self) -> List[str]:
        return list(self._timestamps)

    @property
    def size(self) -> int:
        return len(self._data)

    @property
    def fill_fraction(self) -> float:
        """Fraction of the buffer that is filled (0.0 – 1.0)."""
        return len(self._data) / self._max_size if self._max_size else 0.0

    @property
    def latest(self) -> Optional[float]:
        return self._data[-1] if self._data else None

    @property
    def latest_timestamp(self) -> Optional[str]:
        return self._timestamps[-1] if self._timestamps else None

    def tail(self, n: int) -> List[float]:
        """Return the last *n* values."""
        return list(self._data)[-n:]

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def mean(self, window: Optional[int] = None) -> float:
        """Arithmetic mean over the last *window* values (or all)."""
        data = self.tail(window) if window else list(self._data)
        return sum(data) / len(data) if data else 0.0

    def std(self, window: Optional[int] = None) -> float:
        """Population standard deviation over the last *window* values."""
        data = self.tail(window) if window else list(self._data)
        if len(data) < 2:
            return 0.0
        m = sum(data) / len(data)
        return math.sqrt(sum((x - m) ** 2 for x in data) / len(data))

    def max_value(self, window: Optional[int] = None) -> float:
        data = self.tail(window) if window else list(self._data)
        return max(data) if data else 0.0

    def min_value(self, window: Optional[int] = None) -> float:
        data = self.tail(window) if window else list(self._data)
        return min(data) if data else 0.0

    # ------------------------------------------------------------------
    # Derivatives & smoothing
    # ------------------------------------------------------------------

    def derivative(self, window: int = 1) -> float:
        """First-order finite difference over the last *window* samples.

        Returns the average rate of change per sample.
        """
        if len(self._data) < window + 1:
            return 0.0
        recent = self.tail(window + 1)
        diffs = [recent[i + 1] - recent[i] for i in range(len(recent) - 1)]
        return sum(diffs) / len(diffs)

    def rolling_average(self, window: int = 5) -> float:
        """Simple moving average over the last *window* values."""
        return self.mean(window)

    # ------------------------------------------------------------------
    # Adaptive background (EMA)
    # ------------------------------------------------------------------

    def ema(self, alpha: float = 0.02, seed: Optional[float] = None) -> float:
        """Compute exponential moving average over all buffered values.

        Parameters
        ----------
        alpha : float
            Smoothing factor (0 < alpha < 1). Smaller = smoother.
        seed : float, optional
            Initial EMA value. Defaults to the first observation.
        """
        if not self._data:
            return seed or 0.0
        result = seed if seed is not None else self._data[0]
        for v in self._data:
            result = alpha * v + (1 - alpha) * result
        return result

    def clear(self) -> None:
        self._data.clear()
        self._timestamps.clear()
