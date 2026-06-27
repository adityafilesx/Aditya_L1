export interface QualityFlag {
  status: 'VALID' | 'DEGRADED' | 'WARNING' | 'INTERPOLATED' | 'MISSING' | 'SATURATED' | 'CALIBRATION_WARNING' | 'TIMING_WARNING' | 'REJECTED';
  description: string;
  severity: 'INFO' | 'WARNING' | 'CRITICAL';
  timestamp: string;
  affected_instrument: string;
}

export interface InstrumentMetadata {
  instrument_id: string;
  cadence_hz: number;
  energy_range: string;
  operational_mode: string;
  detector_state: string;
  units: string;
}

export interface ObservationProvenance {
  observation_id: string;
  raw_timestamp: string;
  validation_version: string;
  calibration_version: string;
  sync_version: string;
  pipeline_version: string;
  acquisition_latency_ms: number;
  validation_latency_ms: number;
  calibration_latency_ms: number;
  processing_latency_ms: number;
  total_latency_ms: number;
}

export interface ValidationResult {
  is_valid: boolean;
  packet_integrity_passed: boolean;
  timestamp_continuity_passed: boolean;
  missing_packets: number;
  duplicate_packets: number;
  freshness_ms: number;
}

export interface CalibrationResult {
  is_calibrated: boolean;
  gain_correction_applied: boolean;
  offset_correction_applied: boolean;
  calibration_confidence: number;
}

export interface SynchronizationResult {
  is_synchronized: boolean;
  sync_delay_ms: number;
  time_offset_ms: number;
  sync_confidence: number;
}

export interface NoiseBackgroundResult {
  noise_percentage: number;
  signal_stability: number;
  noise_confidence: number;
  soft_xray_background: number;
  hard_xray_background: number;
}

export interface QualityResult {
  observation_quality: number;
  calibration_confidence: number;
  sync_confidence: number;
  noise_confidence: number;
  overall_scientific_confidence: number;
  flags: QualityFlag[];
}

export interface EnrichedObservation {
  timestamp: string;
  solexs_flux: number;
  helios_flux: number;
  proton_flux: number;
  provenance: ObservationProvenance;
  metadata: Record<string, InstrumentMetadata>;
  validation: ValidationResult;
  calibration: CalibrationResult;
  synchronization: SynchronizationResult;
  noise_background: NoiseBackgroundResult;
  quality: QualityResult;
}

export interface PipelineStatus {
  status: 'GREEN' | 'YELLOW' | 'RED';
  last_updated: string;
  observation_rate_hz: number;
  active_instruments: string[];
  current_latency_ms: number;
  system_health: string;
}

// ---------------------------------------------------------------------------
// Nowcasting Types
// ---------------------------------------------------------------------------

export type DetectorState = 'IDLE' | 'MONITORING' | 'RISING' | 'ACTIVE' | 'PEAK' | 'DECAY' | 'ENDED';

export type FlarePhase = 'WAITING' | 'DETECTED' | 'CONFIRMED' | 'ASSOCIATED' | 'ACTIVE' | 'PEAK' | 'DECAY' | 'COMPLETED' | 'ARCHIVED';

export type AssociationStatus = 'ASSOCIATED' | 'NOT_ASSOCIATED' | 'AMBIGUOUS';

export interface ConfidenceDecomposition {
  peak_ratio_score: number;
  persistence_score: number;
  derivative_score: number;
  quality_score: number;
  overall: number;
}

export interface SolexsEvent {
  event_id: string;
  start_time: string | null;
  peak_time: string | null;
  end_time: string | null;
  peak_flux: number;
  background_flux: number;
  thermal_rise: number;
  detection_confidence: number;
  confidence_decomposition: ConfidenceDecomposition | null;
  quality: string;
  detector_state: DetectorState;
  observation_count: number;
}

export interface HeliosEvent {
  event_id: string;
  start_time: string | null;
  peak_time: string | null;
  end_time: string | null;
  peak_energy: number;
  peak_counts: number;
  burst_duration_s: number;
  detection_confidence: number;
  confidence_decomposition: ConfidenceDecomposition | null;
  detector_state: DetectorState;
  observation_count: number;
}

export interface EventAssociation {
  solexs_event_id: string;
  helios_event_id: string;
  temporal_overlap_s: number;
  neupert_timing_score: number;
  flux_correlation: number;
  association_confidence: number;
  status: AssociationStatus;
}

export interface PhaseTransition {
  from_phase: FlarePhase;
  to_phase: FlarePhase;
  timestamp: string;
  reason: string;
}

// ---------------------------------------------------------------------------
// Physics Engine Types
// ---------------------------------------------------------------------------

export type ComputationStatus = 'GOOD' | 'DEGRADED' | 'INSUFFICIENT' | 'NOT_APPLICABLE';
export type NeupertClassification = 'CONSISTENT' | 'PARTIAL' | 'ANOMALOUS' | 'UNDETERMINED';
export type GOESClass = 'A' | 'B' | 'C' | 'M' | 'X' | 'UNKNOWN';
export type PlasmaState = 'QUIET' | 'HEATING' | 'COOLING' | 'PEAK' | 'UNKNOWN';

export interface ThermalProfile {
  peak_temperature: number;
  temperature_evolution: number[];
  emission_measure: number;
  heating_rate: number;
  cooling_rate: number;
  thermal_energy: number;
  temperature_gradient: number;
}

export interface NonThermalProfile {
  peak_electron_energy: number;
  burst_energy: number;
  hard_xray_energy: number;
  electron_flux: number;
  acceleration_duration: number;
  energy_distribution: number[];
  impulsive_phase_duration: number;
}

export interface SpectralProfile {
  thermal_component: number;
  nonthermal_component: number;
  spectral_residual: number;
  power_law_index: number;
  low_energy_cutoff: number;
  high_energy_cutoff: number;
  goodness_of_fit: number;
}

export interface PlasmaProfile {
  density: number;
  pressure: number;
  energy: number;
  thermal_content: number;
  magnetic_placeholder: number;
  plasma_state: PlasmaState;
}

export interface NeupertProfile {
  neupert_offset: number;
  neupert_score: number;
  neupert_consistency: number;
  neupert_confidence: number;
  neupert_classification: NeupertClassification;
  neupert_timeline: number[];
}

export interface FlareClassification {
  goes_class: GOESClass;
  goes_subclass: string;
  peak_flux: number;
  classification_confidence: number;
  classification_version: string;
}

export interface EventCharacterization {
  start_time: string | null;
  peak_time: string | null;
  end_time: string | null;
  rise_time: number;
  decay_time: number;
  duration: number;
  integrated_flux: number;
  peak_flux: number;
  peak_hard_xray: number;
  peak_soft_xray: number;
  maximum_derivative: number;
  heating_duration: number;
  cooling_duration: number;
  maximum_temperature: number;
  maximum_energy: number;
  background_level: number;
  signal_to_noise_ratio: number;
}

export interface ThermalQuality {
  data_coverage: number;
  sample_count: number;
  min_required_samples: number;
  computation_status: ComputationStatus;
  limiting_factor: string;
}

export interface SpectralQuality {
  fit_residual_norm: number;
  spectral_coverage: number;
  computation_status: ComputationStatus;
  limiting_factor: string;
}

export interface NeupertQuality {
  correlation_validity: number;
  temporal_coverage: number;
  computation_status: ComputationStatus;
  limiting_factor: string;
}

export interface ClassificationQuality {
  flux_measurement_quality: number;
  calibration_confidence: number;
  computation_status: ComputationStatus;
  limiting_factor: string;
}

export interface CharacterizationQuality {
  timing_precision: number;
  snr_adequacy: number;
  computation_status: ComputationStatus;
  limiting_factor: string;
}

export interface PhysicsQuality {
  thermal: ThermalQuality;
  spectral: SpectralQuality;
  neupert: NeupertQuality;
  classification: ClassificationQuality;
  characterization: CharacterizationQuality;
  overall_quality_score: number;
  overall_status: ComputationStatus;
}

export interface PhysicsDerivedIndices {
  heating_index: number;
  cooling_index: number;
  energy_release_index: number;
  thermal_dominance: number;
  neupert_compliance: number;
  spectral_hardness: number;
  impulsiveness_index: number;
}

export interface PhysicsProvenance {
  created_at: string;
  physics_engine_version: string;
  thermal_engine_version: string;
  nonthermal_engine_version: string;
  spectral_engine_version: string;
  plasma_engine_version: string;
  neupert_engine_version: string;
  classification_engine_version: string;
  characterization_engine_version: string;
  indices_engine_version: string;
  observation_ids: string[];
  detector_versions: string[];
  pipeline_version: string;
}

export interface PhysicsCharacterization {
  physics_product_id: string;
  master_id: string;
  thermal: ThermalProfile;
  nonthermal: NonThermalProfile;
  spectral: SpectralProfile;
  plasma: PlasmaProfile;
  neupert: NeupertProfile;
  classification: FlareClassification;
  characterization: EventCharacterization;
  quality: PhysicsQuality;
  indices: PhysicsDerivedIndices;
  provenance: PhysicsProvenance;
  feature_vector_id: string | null;
  forecast_id: string | null;
  explanation_id: string | null;
  decision_id: string | null;
}

export interface DetectorHealthSnapshot {
  detector_name: string;
  alive: boolean;
  fps: number;
  latency_ms: number;
  queue_length: number;
  dropped_frames: number;
  restart_count: number;
  memory_usage_mb: number;
  cpu_usage_percent: number;
}

export interface DetectorBenchmarkSnapshot {
  detector_name: string;
  detection_latency_avg: number;
  false_trigger_rate: number;
  stability: number;
  avg_confidence: number;
  uptime: number;
  avg_event_duration: number;
  missed_detections: number;
  total_events: number;
}

// ---------------------------------------------------------------------------
// Event Lifecycle
// ---------------------------------------------------------------------------

export interface EventLifecycle {
  current_phase: FlarePhase;
  transitions: PhaseTransition[];
  started_at: string | null;
  completed_at: string | null;
}

export interface CatalogProvenance {
  created_at: string;
  last_updated_at: string;
  catalog_version: string;
  pipeline_version: string;
  solexs_detector_version: string;
  helios_detector_version: string;
  association_engine_version: string;
  physics_version: string;
  physics_product_id: string | null;
  observation_ids: string[];
  update_count: number;
  change_log: string[];
}

export interface MasterFlareEntry {
  master_id: string;
  solexs_event: SolexsEvent | null;
  helios_event: HeliosEvent | null;
  association: EventAssociation | null;
  unified_start: string | null;
  unified_peak: string | null;
  unified_end: string | null;
  peak_flux: number;
  peak_energy: number;
  quality: string;
  confidence: number;
  current_state: DetectorState;
  phase: FlarePhase;
  lifecycle: EventLifecycle;
  provenance: CatalogProvenance;
  active_region: string | null;
  physics_product_id: string | null;
  features: Record<string, unknown> | null;
  forecast: Record<string, unknown> | null;
}

export interface DetectorSnapshot {
  detector_name: string;
  state: DetectorState;
  current_flux: number;
  background_level: number;
  threshold: number;
  adaptive_threshold: number;
  confidence: number;
  confidence_decomposition: ConfidenceDecomposition | null;
  buffer_fill: number;
  observation_count: number;
  last_event_id: string | null;
  events_detected: number;
}

export interface NowcastState {
  timestamp: string;
  solexs_detector: DetectorSnapshot;
  helios_detector: DetectorSnapshot;
  active_solexs_event: SolexsEvent | null;
  active_helios_event: HeliosEvent | null;
  active_flare: MasterFlareEntry | null;
  latest_association: EventAssociation | null;
  latest_physics: PhysicsCharacterization | null;
  latest_physics_product_id: string | null;
  latest_classification: FlareClassification | null;
  latest_indices: PhysicsDerivedIndices | null;
  latest_features: any | null;
  latest_feature_vector_id: string | null;
  detector_benchmark_solexs: DetectorBenchmarkSnapshot | null;
  detector_benchmark_helios: DetectorBenchmarkSnapshot | null;
  detector_health_solexs: DetectorHealthSnapshot | null;
  detector_health_helios: DetectorHealthSnapshot | null;
  catalog_total: number;
  catalog_active: number;
  catalog_entries: MasterFlareEntry[];
  timeline: MasterFlareEntry[];
  total_solexs_events: number;
  total_helios_events: number;
  total_associations: number;
}

import { ForecastWindows, ForecastModels } from '../constants/forecastConstants';

export interface ForecastState {
  forecastWindow: ForecastWindows;
  selectedModel: ForecastModels;
  workspace: {
    isScientificExpanded: boolean;
    isAIExpanded: boolean;
    isResearchExpanded: boolean;
  };
  layout: {
    sidebarCollapsed: boolean;
    currentView: 'default' | 'focus' | 'compare';
  };
  filters: {
    minConfidence: number;
    showPrecursorHeating: boolean;
    showHistoricalOverlays: boolean;
  };
  currentObservation: EnrichedObservation | null;
  pipelineStatus: PipelineStatus | null;
  nowcastState: NowcastState | null;
  loading: {
    isModelsLoading: boolean;
    isTelemetryLoading: boolean;
  };
  latestForecast: ForecastOrchestrationResult | null;
}

// ---------------------------------------------------------------------------
// Orchestration & Engine Types
// ---------------------------------------------------------------------------

export interface MultiClassProbabilities {
  A: number;
  B: number;
  C: number;
  M: number;
  X: number;
}

export interface OrchestrationContext {
  timestamp: string;
  active_regions: number;
  current_flux: number;
  data_quality: string;
}

export interface ForecastOrchestrationResult {
  forecast_id: string;
  timestamp: string;
  horizon: string;
  probabilities: MultiClassProbabilities;
  context: OrchestrationContext;
  state: 'QUIET' | 'WATCH' | 'WARNING' | 'ALERT' | 'RECOVERY';
}

