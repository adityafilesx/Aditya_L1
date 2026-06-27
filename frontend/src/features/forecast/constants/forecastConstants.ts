export const ForecastWindows = {
  MIN_15: '15m',
  MIN_30: '30m',
  HR_1: '1h',
  HR_3: '3h',
  HR_6: '6h',
  HR_12: '12h',
  HR_24: '24h',
} as const;

export type ForecastWindows = typeof ForecastWindows[keyof typeof ForecastWindows];

export const ForecastModels = {
  XGBOOST: 'XGBoost-V4',
  TEMPORAL_CN: 'Temporal-CN',
  TRANSFORMER_S: 'Transformer-S',
  HYBRID_ALPHA: 'Hybrid-Alpha',
  ENSEMBLE_CONSENSUS: 'Ensemble Consensus',
} as const;

export type ForecastModels = typeof ForecastModels[keyof typeof ForecastModels];

export const RiskLevels = {
  NOMINAL: 'NOMINAL',
  ELEVATED: 'ELEVATED',
  WATCH: 'WATCH',
  WARNING: 'WARNING',
  ALERT: 'ALERT',
} as const;

export type RiskLevels = typeof RiskLevels[keyof typeof RiskLevels];

export const PredictionClasses = {
  QUIET: 'Quiet',
  A_CLASS: 'A-Class',
  B_CLASS: 'B-Class',
  C_CLASS: 'C-Class',
  M_CLASS: 'M-Class',
  X_CLASS: 'X-Class',
} as const;

export type PredictionClasses = typeof PredictionClasses[keyof typeof PredictionClasses];

export const WidgetOrder = [
  'CurrentPrediction',
  'ForecastHorizon',
  'HighestRisk',
  'ForecastConfidence',
  'ExpectedPeak',
  'SystemHealth',
  'PipelineStatus',
  'LastUpdate',
] as const;

export const ToolbarActions = {
  REFRESH: 'refresh',
  REPLAY: 'replay',
  EXPORT: 'export',
  COMPARE: 'compare',
  SETTINGS: 'settings',
  SEARCH: 'search',
  FILTERS: 'filters',
  LAYOUT: 'layout',
  FULLSCREEN: 'fullscreen',
} as const;

export type ToolbarActions = typeof ToolbarActions[keyof typeof ToolbarActions];
