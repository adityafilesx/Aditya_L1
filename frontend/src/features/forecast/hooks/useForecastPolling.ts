import { useEffect } from 'react';
import { useForecastStore } from '../store/forecastStore';
import { fetchCurrentForecast } from '../../../services/forecast/forecast.service';

const POLLING_INTERVAL = 10000; // 10 seconds

export const useForecastPolling = () => {
  const setLatestForecast = useForecastStore((state) => state.setLatestForecast);

  useEffect(() => {
    let isActive = true;

    const poll = async () => {
      try {
        const forecast = await fetchCurrentForecast();
        if (isActive && forecast) {
          setLatestForecast(forecast);
        }
      } catch (err) {
        console.error('Forecast polling error:', err);
      }
    };

    // Initial fetch
    poll();

    // Setup interval
    const intervalId = setInterval(poll, POLLING_INTERVAL);

    return () => {
      isActive = false;
      clearInterval(intervalId);
    };
  }, [setLatestForecast]);
};
