"""
Configurable detector parameters for the Nowcasting Engine.

All thresholds, buffer sizes, EMA coefficients, and timing windows are
centralised here so that operators can tune detection sensitivity without
touching algorithm code.
"""

import json
import yaml
from pathlib import Path
from pydantic import BaseModel, Field


class SolexsDetectorConfig(BaseModel):
    """Configuration for the SoLEXS soft X-ray thermal flare detector."""

    detector_mode: str = Field(default="AUTO", description="Mode of operation (AUTO, MANUAL, SIMULATION)")
    detector_version: str = Field(default="1.0.0", description="Detector algorithm version")

    # --- Sliding buffer ---
    buffer_size: int = Field(default=120, description="Rolling observation buffer length (samples)")

    # --- Adaptive background (EMA) ---
    ema_alpha: float = Field(default=0.02, description="EMA smoothing factor for background estimation")
    background_seed: float = Field(default=50.0, description="Initial background estimate before enough samples")

    # --- State-transition thresholds (multiples of background) ---
    monitoring_threshold: float = Field(default=1.2, description="Flux / background ratio to enter MONITORING")
    monitoring_persistence: int = Field(default=3, description="Consecutive samples above monitoring_threshold")
    rising_threshold: float = Field(default=1.5, description="Flux / background ratio to enter RISING")
    rising_persistence: int = Field(default=5, description="Consecutive samples with positive derivative in RISING")
    active_threshold: float = Field(default=2.0, description="Flux / background ratio to enter ACTIVE")
    peak_derivative_window: int = Field(default=3, description="Derivative smoothing window for peak detection")
    decay_drop_fraction: float = Field(default=0.20, description="Fraction below peak to enter DECAY")
    ended_threshold: float = Field(default=1.3, description="Flux / background ratio to return to ENDED")

    # --- Derivative ---
    derivative_window: int = Field(default=5, description="Rolling window for derivative computation")
    rolling_avg_window: int = Field(default=5, description="Rolling average smoothing window")

    # --- Confidence decomposition weights ---
    confidence_weight_peak_ratio: float = Field(default=0.35, description="Weight of peak-to-background ratio in confidence")
    confidence_weight_persistence: float = Field(default=0.25, description="Weight of persistence duration in confidence")
    confidence_weight_derivative: float = Field(default=0.20, description="Weight of derivative strength in confidence")
    confidence_weight_quality: float = Field(default=0.20, description="Weight of observation quality in confidence")


class HeliosDetectorConfig(BaseModel):
    """Configuration for the HEL1OS hard X-ray burst detector."""

    detector_mode: str = Field(default="AUTO", description="Mode of operation (AUTO, MANUAL, SIMULATION)")
    detector_version: str = Field(default="1.0.0", description="Detector algorithm version")

    # --- Sliding buffer ---
    buffer_size: int = Field(default=60, description="Rolling observation buffer length (samples)")

    # --- Adaptive background ---
    ema_alpha: float = Field(default=0.05, description="EMA smoothing factor for background estimation")
    background_seed: float = Field(default=10.0, description="Initial background estimate")

    # --- State-transition thresholds (sigma-based) ---
    spike_sigma: float = Field(default=3.0, description="Standard deviations above mean to detect spike")
    rising_persistence: int = Field(default=2, description="Consecutive samples above spike threshold")
    decay_sigma: float = Field(default=2.0, description="Sigma drop from peak to enter DECAY")
    ended_sigma: float = Field(default=1.0, description="Sigma above mean to return to ENDED")

    # --- Burst duration limits ---
    min_burst_duration_s: float = Field(default=2.0, description="Minimum burst duration to be a valid event")
    max_burst_duration_s: float = Field(default=300.0, description="Maximum burst duration before auto-close")

    # --- Confidence decomposition weights ---
    confidence_weight_sigma: float = Field(default=0.40, description="Weight of sigma deviation in confidence")
    confidence_weight_duration: float = Field(default=0.25, description="Weight of burst duration in confidence")
    confidence_weight_energy: float = Field(default=0.20, description="Weight of total energy in confidence")
    confidence_weight_quality: float = Field(default=0.15, description="Weight of observation quality in confidence")


class AssociationConfig(BaseModel):
    """Configuration for the temporal event association engine."""

    temporal_window_s: float = Field(default=120.0, description="Maximum time separation (seconds) for association")
    neupert_max_delay_s: float = Field(default=60.0, description="Max HEL1OS-peak-before-SoLEXS-peak delay for Neupert timing")
    association_threshold: float = Field(default=0.6, description="Confidence above which events are ASSOCIATED")
    ambiguous_threshold: float = Field(default=0.3, description="Confidence above which events are AMBIGUOUS (below = NOT_ASSOCIATED)")

    weight_temporal_overlap: float = Field(default=0.40, description="Weight of temporal overlap in association confidence")
    weight_neupert_timing: float = Field(default=0.35, description="Weight of Neupert timing adherence")
    weight_flux_correlation: float = Field(default=0.25, description="Weight of flux-profile correlation")


class SimulationConfig(BaseModel):
    """Configuration for the flare simulation module."""

    # Quiet-Sun baseline
    solexs_quiet_flux: float = Field(default=30.0, description="Quiet-Sun SoLEXS baseline flux")
    helios_quiet_flux: float = Field(default=8.0, description="Quiet-Sun HEL1OS baseline flux")

    # Flare injection
    flare_probability_per_tick: float = Field(default=0.008, description="Probability of starting a new flare each second")
    flare_min_duration_s: int = Field(default=30, description="Minimum simulated flare duration")
    flare_max_duration_s: int = Field(default=180, description="Maximum simulated flare duration")
    flare_peak_multiplier_min: float = Field(default=3.0, description="Min peak-to-background ratio for simulated flare")
    flare_peak_multiplier_max: float = Field(default=15.0, description="Max peak-to-background ratio for simulated flare")
    helios_spike_delay_s: int = Field(default=0, description="HEL1OS spike precedes SoLEXS by this many seconds (Neupert)")
    helios_burst_fraction: float = Field(default=0.3, description="Fraction of flare duration occupied by HEL1OS burst")

    # Noise
    noise_std_fraction: float = Field(default=0.05, description="Gaussian noise as fraction of quiet baseline")


class PhysicsConfig(BaseModel):
    """Configuration for the Physics Characterization Engine."""
    
    thermal_enabled: bool = True
    nonthermal_enabled: bool = True
    spectral_enabled: bool = True
    plasma_enabled: bool = True
    neupert_enabled: bool = True
    classification_enabled: bool = True
    
    classification_goes_mapping_exponent_offset: float = Field(default=10.0, description="Offset for GOES flux mapping")
    classification_goes_mapping_exponent_scale: float = Field(default=2.0, description="Scale for GOES flux mapping")
    
    neupert_min_correlation: float = Field(default=0.5, description="Min correlation for Neupert consistency")


class NowcastConfig(BaseModel):
    """Top-level configuration aggregating all sub-configs."""

    solexs: SolexsDetectorConfig = Field(default_factory=SolexsDetectorConfig)
    helios: HeliosDetectorConfig = Field(default_factory=HeliosDetectorConfig)
    association: AssociationConfig = Field(default_factory=AssociationConfig)
    simulation: SimulationConfig = Field(default_factory=SimulationConfig)
    physics: PhysicsConfig = Field(default_factory=PhysicsConfig)

    catalog_version: str = Field(default="1.0.0", description="Master Catalog schema version")
    pipeline_version: str = Field(default="1.0.0", description="Nowcast pipeline version")

    @classmethod
    def load_config(cls, path: str) -> 'NowcastConfig':
        """Load configuration from a JSON or YAML file."""
        file_path = Path(path)
        if not file_path.exists():
            return cls()
        
        with open(file_path, "r") as f:
            if file_path.suffix in [".yaml", ".yml"]:
                data = yaml.safe_load(f)
            elif file_path.suffix == ".json":
                data = json.load(f)
            else:
                raise ValueError("Config file must be JSON or YAML")
                
        return cls(**data) if data else cls()


# Global default configuration singleton
nowcast_config = NowcastConfig()
