from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class QualityFlagStatus(str, Enum):
    VALID = "VALID"
    DEGRADED = "DEGRADED"
    WARNING = "WARNING"
    INTERPOLATED = "INTERPOLATED"
    MISSING = "MISSING"
    SATURATED = "SATURATED"
    CALIBRATION_WARNING = "CALIBRATION_WARNING"
    TIMING_WARNING = "TIMING_WARNING"
    REJECTED = "REJECTED"

class QualityFlag(BaseModel):
    status: QualityFlagStatus
    description: str
    severity: str  # "INFO", "WARNING", "CRITICAL"
    timestamp: str
    affected_instrument: str

class InstrumentMetadata(BaseModel):
    instrument_id: str
    cadence_hz: float
    energy_range: str
    operational_mode: str
    detector_state: str
    units: str

class ObservationProvenance(BaseModel):
    observation_id: str
    raw_timestamp: str
    validation_version: str
    calibration_version: str
    sync_version: str
    pipeline_version: str
    acquisition_latency_ms: float
    validation_latency_ms: float
    calibration_latency_ms: float
    processing_latency_ms: float
    total_latency_ms: float

class ValidationResult(BaseModel):
    is_valid: bool
    packet_integrity_passed: bool
    timestamp_continuity_passed: bool
    missing_packets: int
    duplicate_packets: int
    freshness_ms: float

class CalibrationResult(BaseModel):
    is_calibrated: bool
    gain_correction_applied: bool
    offset_correction_applied: bool
    calibration_confidence: float

class SynchronizationResult(BaseModel):
    is_synchronized: bool
    sync_delay_ms: float
    time_offset_ms: float
    sync_confidence: float

class NoiseBackgroundResult(BaseModel):
    noise_percentage: float
    signal_stability: float
    noise_confidence: float
    soft_xray_background: float
    hard_xray_background: float

class QualityResult(BaseModel):
    observation_quality: float
    calibration_confidence: float
    sync_confidence: float
    noise_confidence: float
    overall_scientific_confidence: float
    flags: List[QualityFlag] = []

class EnrichedObservation(BaseModel):
    # Core Data
    timestamp: str
    solexs_flux: float
    helios_flux: float
    proton_flux: float
    
    # Engines outputs
    provenance: ObservationProvenance
    metadata: Dict[str, InstrumentMetadata]
    validation: ValidationResult
    calibration: CalibrationResult
    synchronization: SynchronizationResult
    noise_background: NoiseBackgroundResult
    quality: QualityResult

class PipelineStatus(BaseModel):
    status: str  # "GREEN", "YELLOW", "RED"
    last_updated: str
    observation_rate_hz: float
    active_instruments: List[str]
    current_latency_ms: float
    system_health: str
