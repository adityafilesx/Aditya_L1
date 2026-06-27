import { useForecastStore } from '../store/forecastStore';

export const useForecast = () => {
  const currentObservation = useForecastStore((state) => state.currentObservation);
  const pipelineStatus = useForecastStore((state) => state.pipelineStatus);
  const forecastWindow = useForecastStore((state) => state.forecastWindow);
  const setForecastWindow = useForecastStore((state) => state.setForecastWindow);
  const selectedModel = useForecastStore((state) => state.selectedModel);
  const setSelectedModel = useForecastStore((state) => state.setSelectedModel);
  const loading = useForecastStore((state) => state.loading);
  const latestForecast = useForecastStore((state) => state.latestForecast);

  return {
    currentObservation,
    pipelineStatus,
    forecastWindow,
    setForecastWindow,
    selectedModel,
    setSelectedModel,
    loading,
    latestForecast,
  };
};

export const useForecastLayout = () => {
  const layout = useForecastStore((state) => state.layout);
  return { layout };
};

export const useForecastWorkspace = () => {
  const workspace = useForecastStore((state) => state.workspace);
  const toggleScientificExpanded = useForecastStore((state) => state.toggleScientificExpanded);
  const toggleAIExpanded = useForecastStore((state) => state.toggleAIExpanded);
  const toggleResearchExpanded = useForecastStore((state) => state.toggleResearchExpanded);

  return {
    workspace,
    toggleScientificExpanded,
    toggleAIExpanded,
    toggleResearchExpanded,
  };
};
