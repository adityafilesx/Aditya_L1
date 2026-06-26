import { create } from 'zustand';

// Type definitions for the global MissionState
export interface TelemetryState {
  solexs_sdd2_ctr: number;
  helios_czt_broad_ctr: number;
  goes_xrs_b: number;
  goes_xrs_a: number;
  proton_flux_10MeV: number;
  timestamp: string;
}

export interface PhysicsState {
  temperature_mk: number;
  emission_measure_norm: number;
  neupert_score: number;
  spectral_centroid: number;
  shannon_entropy: number;
  spectral_flatness: number;
  spectral_rolloff: number;
}

export interface ForecastState {
  probability: number;
  confidence: number;
  estimated_goes_class: string;
}

export interface ModelState {
  ensemble_status: string;
  xgb_status: string;
  ai_temporal_status: string;
}

export interface AlertEvent {
  id: string;
  timestamp: string;
  severity: string;
  type: string;
  description: string;
}

export interface DigitalTwinState {
  active_region: string;
  similarity_score: number;
  flux_delta: number;
  v_field_delta: number;
  temp_delta: number;
}

export interface MissionState {
  state: number; // 0: Nominal, 1: Watch, 2: Alert
  mode: string;
  operator: string;
  clock_utc: string;
  telemetry: TelemetryState;
  physics: PhysicsState;
  forecast: ForecastState;
  models: ModelState;
  sensors: Record<string, string>;
  system_metrics: Record<string, number>;
  digital_twin: DigitalTwinState;
  alerts: AlertEvent[];
  recommendations: string[];
  confidence_bounds: number[];
}

interface StreamStore {
  mission: MissionState | null;
  history: {
    telemetry: TelemetryState[];
    physics: PhysicsState[];
  };
  connectionStatus: 'connecting' | 'connected' | 'disconnected' | 'reconnecting';
  
  // Actions
  setMissionState: (state: MissionState) => void;
  updateTelemetry: (telemetry: TelemetryState) => void;
  updatePhysics: (physics: PhysicsState) => void;
  updateForecast: (forecast: ForecastState) => void;
  updateDigitalTwin: (dt: DigitalTwinState) => void;
  updateSystem: (metrics: Record<string, number>) => void;
  addAlert: (alert: AlertEvent) => void;
  setConnectionStatus: (status: 'connecting' | 'connected' | 'disconnected' | 'reconnecting') => void;
}

export const useStreamStore = create<StreamStore>((set) => ({
  mission: null,
  history: { telemetry: [], physics: [] },
  connectionStatus: 'disconnected',

  setMissionState: (state) => set((prev) => ({
    mission: state,
    history: {
      telemetry: [...prev.history.telemetry, state.telemetry].slice(-100),
      physics: [...prev.history.physics, state.physics].slice(-100)
    }
  })),
  
  updateTelemetry: (telemetry) => set((state) => ({
    mission: state.mission ? { ...state.mission, telemetry } : null,
    history: {
      ...state.history,
      telemetry: [...state.history.telemetry, telemetry].slice(-100)
    }
  })),
  
  updatePhysics: (physics) => set((state) => ({
    mission: state.mission ? { ...state.mission, physics } : null,
    history: {
      ...state.history,
      physics: [...state.history.physics, physics].slice(-100)
    }
  })),
  
  updateForecast: (forecast) => set((state) => ({
    mission: state.mission ? { ...state.mission, forecast } : null
  })),
  
  updateDigitalTwin: (dt) => set((state) => ({
    mission: state.mission ? { ...state.mission, digital_twin: dt } : null
  })),
  
  updateSystem: (metrics) => set((state) => ({
    mission: state.mission ? { ...state.mission, system_metrics: metrics } : null
  })),
  
  addAlert: (alert) => set((state) => {
    if (!state.mission) return state;
    // Keep max 20 alerts
    const newAlerts = [alert, ...state.mission.alerts].slice(0, 20);
    return { mission: { ...state.mission, alerts: newAlerts } };
  }),
  
  setConnectionStatus: (status) => set({ connectionStatus: status }),
}));
