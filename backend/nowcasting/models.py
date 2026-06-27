"""
Pydantic models for the Scientific Nowcasting Engine.

Covers detector states, flare events, association results, the Master Flare
Catalog (with provenance & versioning), detector snapshots, and the complete
NowcastState transmitted over WebSocket.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class DetectorState(str, Enum):
    IDLE = "IDLE"
    MONITORING = "MONITORING"
    RISING = "RISING"
    ACTIVE = "ACTIVE"
    PEAK = "PEAK"
    DECAY = "DECAY"
    ENDED = "ENDED"


class FlarePhase(str, Enum):
    WAITING = "WAITING"
    DETECTED = "DETECTED"
    CONFIRMED = "CONFIRMED"
    ASSOCIATED = "ASSOCIATED"
    ACTIVE = "ACTIVE"
    PEAK = "PEAK"
    DECAY = "DECAY"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class AssociationStatus(str, Enum):
    ASSOCIATED = "ASSOCIATED"
    NOT_ASSOCIATED = "NOT_ASSOCIATED"
    AMBIGUOUS = "AMBIGUOUS"


# ---------------------------------------------------------------------------
# Confidence Decomposition
# ---------------------------------------------------------------------------

class ConfidenceDecomposition(BaseModel):
    """Breakdown of how a detector's overall confidence score is composed."""
    peak_ratio_score: float = 0.0
    persistence_score: float = 0.0
    derivative_score: float = 0.0
    quality_score: float = 0.0
    overall: float = 0.0


# ---------------------------------------------------------------------------
# Detector Events
# ---------------------------------------------------------------------------

class SolexsEvent(BaseModel):
    """A complete soft X-ray flare event detected by the SoLEXS detector."""
    event_id: str = Field(default_factory=lambda: f"SOL-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}")
    start_time: Optional[str] = None
    peak_time: Optional[str] = None
    end_time: Optional[str] = None
    peak_flux: float = 0.0
    background_flux: float = 0.0
    thermal_rise: float = 0.0
    detection_confidence: float = 0.0
    confidence_decomposition: Optional[ConfidenceDecomposition] = None
    quality: str = "UNKNOWN"   # GOOD / DEGRADED / POOR / UNKNOWN
    detector_state: DetectorState = DetectorState.IDLE
    observation_count: int = 0


class HeliosEvent(BaseModel):
    """A complete hard X-ray burst event detected by the HEL1OS detector."""
    event_id: str = Field(default_factory=lambda: f"HEL-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}")
    start_time: Optional[str] = None
    peak_time: Optional[str] = None
    end_time: Optional[str] = None
    peak_energy: float = 0.0
    peak_counts: float = 0.0
    burst_duration_s: float = 0.0
    detection_confidence: float = 0.0
    confidence_decomposition: Optional[ConfidenceDecomposition] = None
    detector_state: DetectorState = DetectorState.IDLE
    observation_count: int = 0


# ---------------------------------------------------------------------------
# Event Association
# ---------------------------------------------------------------------------

class EventAssociation(BaseModel):
    """Result of temporally associating a SoLEXS event with a HEL1OS event."""
    solexs_event_id: str
    helios_event_id: str
    temporal_overlap_s: float = 0.0
    neupert_timing_score: float = 0.0
    flux_correlation: float = 0.0
    association_confidence: float = 0.0
    status: AssociationStatus = AssociationStatus.NOT_ASSOCIATED


# ---------------------------------------------------------------------------
# Event Lifecycle
# ---------------------------------------------------------------------------

class PhaseTransition(BaseModel):
    """A single phase transition with timestamp."""
    from_phase: FlarePhase
    to_phase: FlarePhase
    timestamp: str
    reason: str = ""


class EventLifecycle(BaseModel):
    """Complete lifecycle tracking for a flare event."""
    current_phase: FlarePhase = FlarePhase.WAITING
    transitions: List[PhaseTransition] = []
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Master Flare Catalog Entry  (with provenance & versioning)
# ---------------------------------------------------------------------------

class CatalogProvenance(BaseModel):
    """Provenance record for a Master Catalog entry."""
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    last_updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    catalog_version: str = "1.0.0"
    pipeline_version: str = "1.0.0"
    solexs_detector_version: str = "1.0.0"
    helios_detector_version: str = "1.0.0"
    association_engine_version: str = "1.0.0"
    physics_version: str = "1.0.0"
    physics_product_id: Optional[str] = None
    feature_vector_id: Optional[str] = None
    observation_ids: List[str] = []
    update_count: int = 0
    change_log: List[str] = []


class MasterFlareEntry(BaseModel):
    """A single entry in the Unified Master Flare Catalog."""
    master_id: str = ""
    solexs_event: Optional[SolexsEvent] = None
    helios_event: Optional[HeliosEvent] = None
    association: Optional[EventAssociation] = None

    # Unified timing
    unified_start: Optional[str] = None
    unified_peak: Optional[str] = None
    unified_end: Optional[str] = None

    # Unified metrics
    peak_flux: float = 0.0
    peak_energy: float = 0.0
    quality: str = "UNKNOWN"
    confidence: float = 0.0
    current_state: DetectorState = DetectorState.IDLE
    phase: FlarePhase = FlarePhase.WAITING

    # Lifecycle
    lifecycle: EventLifecycle = Field(default_factory=EventLifecycle)

    # Provenance & versioning
    provenance: CatalogProvenance = Field(default_factory=CatalogProvenance)

    # Placeholders for future milestones
    active_region: Optional[str] = None
    physics_product_id: Optional[str] = None
    feature_vector_id: Optional[str] = None
    features: Optional[Dict] = None
    forecast: Optional[Dict] = None


# ---------------------------------------------------------------------------
# Detector Snapshots (live state exposed to frontend)
# ---------------------------------------------------------------------------

class DetectorSnapshot(BaseModel):
    """Real-time snapshot of a single detector's internal state."""
    detector_name: str
    state: DetectorState = DetectorState.IDLE
    current_flux: float = 0.0
    background_level: float = 0.0
    threshold: float = 0.0
    adaptive_threshold: float = 0.0
    confidence: float = 0.0
    confidence_decomposition: Optional[ConfidenceDecomposition] = None
    buffer_fill: float = 0.0   # 0.0 – 1.0 fraction of buffer filled
    observation_count: int = 0
    last_event_id: Optional[str] = None
    events_detected: int = 0


class DetectorHealthSnapshot(BaseModel):
    """Real-time health status of a detector."""
    detector_name: str
    alive: bool = True
    fps: float = 0.0
    latency_ms: float = 0.0
    queue_length: int = 0
    dropped_frames: int = 0
    restart_count: int = 0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0


class DetectorBenchmarkSnapshot(BaseModel):
    """Real-time benchmark snapshot of a detector."""
    detector_name: str
    detection_latency_avg: float = 0.0
    false_trigger_rate: float = 0.0
    stability: float = 1.0
    avg_confidence: float = 0.0
    uptime: float = 0.0
    avg_event_duration: float = 0.0
    missed_detections: int = 0
    total_events: int = 0


# ---------------------------------------------------------------------------
# Aggregate Nowcast State (transmitted via WebSocket)
# ---------------------------------------------------------------------------

class NowcastState(BaseModel):
    """Complete nowcasting system snapshot streamed to the frontend."""
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    # Detector snapshots
    solexs_detector: DetectorSnapshot = Field(default_factory=lambda: DetectorSnapshot(detector_name="SoLEXS"))
    helios_detector: DetectorSnapshot = Field(default_factory=lambda: DetectorSnapshot(detector_name="HEL1OS"))

    # Active events (currently in progress)
    active_solexs_event: Optional[SolexsEvent] = None
    active_helios_event: Optional[HeliosEvent] = None
    active_flare: Optional[MasterFlareEntry] = None

    # Latest completed association
    latest_association: Optional[EventAssociation] = None

    # Physics State
    latest_physics: Optional[Any] = None
    latest_physics_product_id: Optional[str] = None
    latest_classification: Optional[Any] = None
    latest_indices: Optional[Any] = None
    latest_features: Optional[Any] = None
    latest_feature_vector_id: Optional[str] = None
    
    # Benchmarks & Health
    detector_benchmark_solexs: Optional[DetectorBenchmarkSnapshot] = None
    detector_benchmark_helios: Optional[DetectorBenchmarkSnapshot] = None
    detector_health_solexs: Optional[DetectorHealthSnapshot] = None
    detector_health_helios: Optional[DetectorHealthSnapshot] = None

    # Catalog summary
    catalog_total: int = 0
    catalog_active: int = 0
    catalog_entries: List[MasterFlareEntry] = []

    # Timeline (last 20 events)
    timeline: List[MasterFlareEntry] = []

    # Counters
    total_solexs_events: int = 0
    total_helios_events: int = 0
    total_associations: int = 0
