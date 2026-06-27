/**
 * Forecast Service
 * Connects to Backend Machine Learning predictions (XGBoost/LightGBM) via Orchestrator.
 */
import type { ForecastOrchestrationResult } from '../../features/forecast/types/ForecastTypes';

export const fetchCurrentForecast = async (): Promise<ForecastOrchestrationResult | null> => {
  try {
    // The backend runs on localhost:8000
    const response = await fetch('http://localhost:8000/api/forecast/current');
    
    if (!response.ok) {
      console.warn(`Forecast fetch failed with status: ${response.status}`);
      return null;
    }

    const data = await response.json();
    if (data.status && data.status.includes('No forecasts available')) {
       return null;
    }
    
    return data as ForecastOrchestrationResult;
  } catch (error) {
    console.error('Error fetching forecast:', error);
    return null;
  }
};
