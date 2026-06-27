import { create } from 'zustand';
import type { ForecastState, EnrichedObservation, PipelineStatus, NowcastState } from '../types/ForecastTypes';
import { ForecastWindows, ForecastModels } from '../constants/forecastConstants';

interface ForecastStore extends ForecastState {
  setForecastWindow: (window: ForecastWindows) => void;
  setSelectedModel: (model: ForecastModels) => void;
  setWorkspaceState: (workspace: Partial<ForecastState['workspace']>) => void;
  setLayoutState: (layout: Partial<ForecastState['layout']>) => void;
  setFilters: (filters: Partial<ForecastState['filters']>) => void;
  setObservation: (observation: EnrichedObservation | null) => void;
  setPipelineStatus: (status: PipelineStatus | null) => void;
  setNowcastState: (state: NowcastState | null) => void;
  setLatestForecast: (forecast: any | null) => void;
  toggleScientificExpanded: () => void;
  toggleAIExpanded: () => void;
  toggleResearchExpanded: () => void;
}

export const useForecastStore = create<ForecastStore>((set) => ({
  // Defaults
  forecastWindow: ForecastWindows.HR_24,
  selectedModel: ForecastModels.ENSEMBLE_CONSENSUS,
  workspace: {
    isScientificExpanded: false,
    isAIExpanded: false,
    isResearchExpanded: false,
  },
  layout: {
    sidebarCollapsed: false,
    currentView: 'default',
  },
  filters: {
    minConfidence: 0.75,
    showPrecursorHeating: true,
    showHistoricalOverlays: false,
  },
  currentObservation: null,
  pipelineStatus: null,
  nowcastState: null,
  loading: {
    isModelsLoading: false,
    isTelemetryLoading: false,
  },
  latestForecast: null,

  // Actions
  setForecastWindow: (window) => set({ forecastWindow: window }),
  setSelectedModel: (model) => set({ selectedModel: model }),
  
  setWorkspaceState: (workspace) => set((state) => ({ 
    workspace: { ...state.workspace, ...workspace } 
  })),
  
  setLayoutState: (layout) => set((state) => ({ 
    layout: { ...state.layout, ...layout } 
  })),
  
  setFilters: (filters) => set((state) => ({ 
    filters: { ...state.filters, ...filters } 
  })),

  setObservation: (observation) => set({ currentObservation: observation }),
  setPipelineStatus: (status) => set({ pipelineStatus: status }),
  setNowcastState: (nowcastState) => set({ nowcastState }),
  setLatestForecast: (forecast) => set({ latestForecast: forecast }),

  toggleScientificExpanded: () => set((state) => ({ 
    workspace: { ...state.workspace, isScientificExpanded: !state.workspace.isScientificExpanded } 
  })),
  
  toggleAIExpanded: () => set((state) => ({ 
    workspace: { ...state.workspace, isAIExpanded: !state.workspace.isAIExpanded } 
  })),
  
  toggleResearchExpanded: () => set((state) => ({ 
    workspace: { ...state.workspace, isResearchExpanded: !state.workspace.isResearchExpanded } 
  })),
}));
