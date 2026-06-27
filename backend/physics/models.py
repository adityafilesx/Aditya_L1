"""
Pydantic models for the Physics Characterization Engine.

Defines strongly-typed models for every physics sub-engine output, quality
assessments, derived indices, provenance, and the top-level
PhysicsCharacterization product.

Design Principles
-----------------
- **Reference by ID**: The Master Flare Catalog stores only a
  ``physics_product_id`` string; the full product lives here.
- **Quality ≠ Confidence**: Each sub-engine produces a separate quality
  assessment describing the fitness of the *computation* itself.
- **Derived Indices**: Pre-computed dimensionless ratios that become direct
  ML features in Milestone 4.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class ComputationStatus(str, Enum):
    GOOD = "GOOD"
    DEGRADED = "DEGRADED"
    INSUFFICIENT = "INSUFFICIENT"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class NeupertClassification(str, Enum):
    CONSISTENT = "CONSISTENT"
    PARTIAL = "PARTIAL"
    ANOMALOUS = "ANOMALOUS"
    UNDETERMINED = "UNDETERMINED"


class GOESClass(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    M = "M"
    X = "X"
    UNKNOWN = "UNKNOWN"


class PlasmaState(str, Enum):
    QUIET = "QUIET"
    HEATING = "HEATING"
    COOLING = "COOLING"
    PEAK = "PEAK"
    UNKNOWN = "UNKNOWN"


# ---------------------------------------------------------------------------
# Core Physics Profile Models
# ---------------------------------------------------------------------------

class ThermalProfile(BaseModel):
    """Thermal characterization of a solar flare."""
    peak_temperature: float = 0.0           # MK
    temperature_evolution: List[float] = []  # time-series of T(t) in MK
    emission_measure: float = 0.0           # cm⁻³ (log scale)
    heating_rate: float = 0.0               # MK/s
    cooling_rate: float = 0.0               # MK/s
    thermal_energy: float = 0.0             # erg
    temperature_gradient: float = 0.0       # MK per sample


class NonThermalProfile(BaseModel):
    """Non-thermal (hard X-ray) characterization."""
    peak_electron_energy: float = 0.0       # keV
    burst_energy: float = 0.0               # integrated counts
    hard_xray_energy: float = 0.0           # erg
    electron_flux: float = 0.0              # electrons/s/cm²
    acceleration_duration: float = 0.0      # seconds
    energy_distribution: List[float] = []   # energy vs time
    impulsive_phase_duration: float = 0.0   # seconds


class SpectralProfile(BaseModel):
    """Spectral decomposition of the flare emission."""
    thermal_component: float = 0.0          # fractional contribution
    nonthermal_component: float = 0.0       # fractional contribution
    spectral_residual: float = 0.0          # fit residual
    power_law_index: float = 0.0            # γ
    low_energy_cutoff: float = 0.0          # keV
    high_energy_cutoff: float = 0.0         # keV
    goodness_of_fit: float = 0.0            # 0–1


class PlasmaProfile(BaseModel):
    """Plasma state characterization."""
    density: float = 0.0                    # cm⁻³
    pressure: float = 0.0                   # dyne/cm²
    energy: float = 0.0                     # erg
    thermal_content: float = 0.0            # erg
    magnetic_placeholder: float = 0.0       # Gauss (placeholder)
    plasma_state: PlasmaState = PlasmaState.UNKNOWN


class NeupertProfile(BaseModel):
    """Neupert effect analysis."""
    neupert_offset: float = 0.0             # seconds (HEL1OS peak → SoLEXS peak)
    neupert_score: float = 0.0              # 0–1 correlation
    neupert_consistency: float = 0.0        # 0–1
    neupert_confidence: float = 0.0         # 0–1
    neupert_classification: NeupertClassification = NeupertClassification.UNDETERMINED
    neupert_timeline: List[float] = []      # cumulative integral time-series


class FlareClassification(BaseModel):
    """Observed GOES flare classification."""
    goes_class: GOESClass = GOESClass.UNKNOWN
    goes_subclass: str = ""                 # e.g. "M2.3"
    peak_flux: float = 0.0                  # W/m² equivalent
    classification_confidence: float = 0.0  # 0–1
    classification_version: str = "1.0.0"


class EventCharacterization(BaseModel):
    """Complete temporal characterization of a flare event."""
    start_time: Optional[str] = None
    peak_time: Optional[str] = None
    end_time: Optional[str] = None
    rise_time: float = 0.0                  # seconds
    decay_time: float = 0.0                 # seconds
    duration: float = 0.0                   # seconds
    integrated_flux: float = 0.0            # counts × s
    peak_flux: float = 0.0
    peak_hard_xray: float = 0.0
    peak_soft_xray: float = 0.0
    maximum_derivative: float = 0.0         # dFlux/dt max
    heating_duration: float = 0.0           # seconds
    cooling_duration: float = 0.0           # seconds
    maximum_temperature: float = 0.0        # MK
    maximum_energy: float = 0.0             # erg
    background_level: float = 0.0
    signal_to_noise_ratio: float = 0.0


# ---------------------------------------------------------------------------
# Per-Engine Quality Models (Quality ≠ Confidence)
# ---------------------------------------------------------------------------

class ThermalQuality(BaseModel):
    """Quality of the thermal computation."""
    data_coverage: float = 0.0              # 0–1 fraction of expected samples
    sample_count: int = 0
    min_required_samples: int = 10
    computation_status: ComputationStatus = ComputationStatus.NOT_APPLICABLE
    limiting_factor: str = ""


class SpectralQuality(BaseModel):
    """Quality of the spectral fit."""
    fit_residual_norm: float = 0.0
    spectral_coverage: float = 0.0          # 0–1
    computation_status: ComputationStatus = ComputationStatus.NOT_APPLICABLE
    limiting_factor: str = ""


class NeupertQuality(BaseModel):
    """Quality of the Neupert analysis."""
    correlation_validity: float = 0.0       # 0–1
    temporal_coverage: float = 0.0          # 0–1
    computation_status: ComputationStatus = ComputationStatus.NOT_APPLICABLE
    limiting_factor: str = ""


class ClassificationQuality(BaseModel):
    """Quality of the GOES classification."""
    flux_measurement_quality: float = 0.0   # 0–1
    calibration_confidence: float = 0.0     # 0–1
    computation_status: ComputationStatus = ComputationStatus.NOT_APPLICABLE
    limiting_factor: str = ""


class CharacterizationQuality(BaseModel):
    """Quality of the temporal characterization."""
    timing_precision: float = 0.0           # 0–1
    snr_adequacy: float = 0.0              # 0–1
    computation_status: ComputationStatus = ComputationStatus.NOT_APPLICABLE
    limiting_factor: str = ""


class PhysicsQuality(BaseModel):
    """Aggregated quality across all physics sub-engines."""
    thermal: ThermalQuality = Field(default_factory=ThermalQuality)
    spectral: SpectralQuality = Field(default_factory=SpectralQuality)
    neupert: NeupertQuality = Field(default_factory=NeupertQuality)
    classification: ClassificationQuality = Field(default_factory=ClassificationQuality)
    characterization: CharacterizationQuality = Field(default_factory=CharacterizationQuality)
    overall_quality_score: float = 0.0      # 0–1 weighted average
    overall_status: ComputationStatus = ComputationStatus.NOT_APPLICABLE


# ---------------------------------------------------------------------------
# Derived Physics Indices (direct ML features)
# ---------------------------------------------------------------------------

class PhysicsDerivedIndices(BaseModel):
    """Pre-computed dimensionless indices for downstream ML feature engineering."""
    heating_index: float = 0.0              # heating_rate / cooling_rate
    cooling_index: float = 0.0              # decay_time / rise_time
    energy_release_index: float = 0.0       # log10(thermal + nonthermal energy)
    thermal_dominance: float = 0.0          # thermal_energy / total_energy  (0–1)
    neupert_compliance: float = 0.0         # neupert_score × neupert_consistency (0–1)
    spectral_hardness: float = 0.0          # 1 / power_law_index (0–1 clamped)
    impulsiveness_index: float = 0.0        # peak_flux / (integrated_flux / duration)


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------

class PhysicsProvenance(BaseModel):
    """Full lineage for a physics product."""
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    physics_engine_version: str = "1.0.0"
    thermal_engine_version: str = "1.0.0"
    nonthermal_engine_version: str = "1.0.0"
    spectral_engine_version: str = "1.0.0"
    plasma_engine_version: str = "1.0.0"
    neupert_engine_version: str = "1.0.0"
    classification_engine_version: str = "1.0.0"
    characterization_engine_version: str = "1.0.0"
    indices_engine_version: str = "1.0.0"
    observation_ids: List[str] = []
    detector_versions: List[str] = []
    pipeline_version: str = "1.0.0"


# ---------------------------------------------------------------------------
# Top-Level Physics Product
# ---------------------------------------------------------------------------

class PhysicsCharacterization(BaseModel):
    """Complete physics characterization product for a single flare.

    This is the top-level object stored in the PhysicsRepository.
    The Master Flare Catalog stores only ``physics_product_id`` as a reference.
    """
    # Identity
    physics_product_id: str = ""            # PHY-YYYYMMDD-NNN
    master_id: str = ""                     # back-reference to MasterFlareEntry

    # Physics profiles
    thermal: ThermalProfile = Field(default_factory=ThermalProfile)
    nonthermal: NonThermalProfile = Field(default_factory=NonThermalProfile)
    spectral: SpectralProfile = Field(default_factory=SpectralProfile)
    plasma: PlasmaProfile = Field(default_factory=PlasmaProfile)
    neupert: NeupertProfile = Field(default_factory=NeupertProfile)
    classification: FlareClassification = Field(default_factory=FlareClassification)
    characterization: EventCharacterization = Field(default_factory=EventCharacterization)

    # Quality (separate from confidence)
    quality: PhysicsQuality = Field(default_factory=PhysicsQuality)

    # Derived indices (ML-ready features)
    indices: PhysicsDerivedIndices = Field(default_factory=PhysicsDerivedIndices)

    # Provenance
    provenance: PhysicsProvenance = Field(default_factory=PhysicsProvenance)

    # Future downstream references (populated by later milestones)
    feature_vector_id: Optional[str] = None
    forecast_id: Optional[str] = None
    explanation_id: Optional[str] = None
    decision_id: Optional[str] = None
