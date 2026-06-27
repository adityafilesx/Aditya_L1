import { useEffect } from 'react';
import { useForecastStore } from '../store/forecastStore';

export const useObservationStream = () => {
  const { setObservation, setPipelineStatus } = useForecastStore();

  useEffect(() => {
    // In production this would use environment variables
    const wsUrl = `ws://localhost:8000/ws/observation/stream`;
    
    let ws: WebSocket;
    let reconnectTimeout: NodeJS.Timeout;

    const connect = () => {
      ws = new WebSocket(wsUrl);

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          if (message.type === 'observation') {
            setObservation(message.data);
          } else if (message.type === 'pipeline_status') {
            setPipelineStatus(message.data);
          }
        } catch (e) {
          console.error('Failed to parse observation stream data', e);
        }
      };

      ws.onerror = (error) => {
        console.error('Observation Stream WS Error:', error);
      };

      ws.onclose = () => {
        console.log('Observation Stream closed. Reconnecting...');
        reconnectTimeout = setTimeout(connect, 3000);
      };
    };

    connect();

    return () => {
      if (ws) {
        ws.close();
      }
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
      }
    };
  }, [setObservation, setPipelineStatus]);
};
