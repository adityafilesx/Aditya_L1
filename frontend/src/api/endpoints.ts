import { fetchClient } from "./client";

// Types will be imported from src/types once defined

export const api = {
  dashboard: {
    getDashboard: () => fetchClient<any>("/dashboard/"),
  },
  operations: {
    getTelemetry: () => fetchClient<any>("/operations/telemetry"),
    getPhysics: () => fetchClient<any>("/operations/physics"),
    getHealth: () => fetchClient<any>("/operations/health"),
    getModels: () => fetchClient<any>("/operations/models"),
  },
  forecast: {
    getCurrent: () => fetchClient<any>("/forecast/current"),
    getHorizons: () => fetchClient<any>("/forecast/horizons"),
  },
  physics: {
    getSummary: () => fetchClient<any>("/physics/summary"),
  },
  decision: {
    getState: () => fetchClient<any>("/decision/state"),
    getAlerts: () => fetchClient<any>("/decision/alerts"),
    getThresholds: () => fetchClient<any>("/decision/thresholds"),
    getDrift: () => fetchClient<any>("/decision/drift"),
  },
  digitalTwin: {
    getState: () => fetchClient<any>("/digital-twin/state"),
    getActiveRegions: () => fetchClient<any>("/digital-twin/active-regions"),
    getSimilarity: (arNum: number) => fetchClient<any>(`/digital-twin/similarity/${arNum}`),
  },
  knowledgeGraph: {
    getSummary: () => fetchClient<any>("/knowledge-graph/"),
    getEvents: () => fetchClient<any>("/knowledge-graph/events"),
  },
  intelligence: {
    getRisk: () => fetchClient<any>("/intelligence/risk"),
    getRecommendations: () => fetchClient<any>("/intelligence/recommendations"),
  },
  system: {
    getHealth: () => fetchClient<any>("/system/health"),
    getConfig: () => fetchClient<any>("/system/config"),
    getDiagnostics: () => fetchClient<any>("/system/diagnostics"),
  },
  timeline: {
    getEvents: () => fetchClient<any>("/timeline/events"),
    getAlerts: () => fetchClient<any>("/timeline/alerts"),
  },
  research: {
    getBenchmarks: () => fetchClient<any>("/research/benchmarks"),
    getExplainability: () => fetchClient<any>("/research/explainability"),
  },
  ml: {
    getRegistry: () => fetchClient<any>("/ml/registry"),
    getModels: () => fetchClient<any>("/ml/models"),
    getCalibration: () => fetchClient<any>("/ml/calibration"),
    getTargets: () => fetchClient<any>("/ml/targets"),
    getMetrics: () => fetchClient<any>("/ml/metrics"),
    getMonitoring: () => fetchClient<any>("/ml/monitoring"),
  },
  features: {
    getRegistry: () => fetchClient<any>("/features/registry"),
  }
};
