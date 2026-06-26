/**
 * Forecast Service (Phase FE-5 Draft)
 * Connects to Backend Machine Learning predictions (XGBoost/LightGBM).
 */

export interface ForecastResponse {
  probability_M_class: number;
  probability_X_class: number;
  flare_expected_window: string;
  confidence: number;
}

export const fetchNowcast = async (): Promise<ForecastResponse> => {
  // TODO: Implement actual fetch using VITE_API_BASE_URL
  console.warn("ForecastService.fetchNowcast: API not yet integrated. Returning mock data.");
  return {
    probability_M_class: 0.85,
    probability_X_class: 0.12,
    flare_expected_window: "2-4h",
    confidence: 0.94
  };
};
