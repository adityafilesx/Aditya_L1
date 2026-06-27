import { useEffect, useRef, useState } from 'react';
import { useForecastStore } from '../store/forecastStore';

const WS_URL = 'ws://localhost:8000/ws/nowcasting/stream';
const RECONNECT_DELAY = 2000;

export function useNowcastStream() {
  const ws = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<NodeJS.Timeout | undefined>(undefined);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const setNowcastState = useForecastStore(state => state.setNowcastState);

  const connect = () => {
    try {
      if (ws.current?.readyState === WebSocket.OPEN) return;

      ws.current = new WebSocket(WS_URL);

      ws.current.onopen = () => {
        setIsConnected(true);
        setError(null);
      };

      ws.current.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.type === 'nowcast_state') {
            setNowcastState(payload.data);
          }
        } catch (e) {
          console.error('Failed to parse nowcast stream message', e);
        }
      };

      ws.current.onclose = () => {
        setIsConnected(false);
        ws.current = null;
        // Auto-reconnect
        reconnectTimeout.current = setTimeout(connect, RECONNECT_DELAY);
      };

      ws.current.onerror = () => {
        setError('WebSocket error occurred');
        ws.current?.close();
      };
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to connect');
    }
  };

  useEffect(() => {
    connect();
    return () => {
      if (reconnectTimeout.current) clearTimeout(reconnectTimeout.current);
      if (ws.current) {
        ws.current.close();
        ws.current = null;
      }
    };
  }, []);

  return { isConnected, error };
}
