from typing import Dict, List, Optional, Any
from pydantic import BaseModel

class FeatureRegistryEntry(BaseModel):
    feature_id: str
    name: str
    description: str
    scientific_meaning: str
    units: str
    category: str
    source_engine: str
    source_variables: List[str]
    dependencies: List[str]
    calculation_method: str
    normalization_strategy: str  # "minmax" or "standard" or "none"
    allowed_range: tuple[float, float]
    expected_distribution: str  # "normal", "lognormal", "uniform", etc.
    quality_rules: Dict[str, Any]
    version: str = "1.0.0"
    introduced_in: str = "4.5"
    deprecated: bool = False
    future_ml_models: List[str] = []
    future_explainability: bool = True
    forecast_target_usage: List[str] = []


class FeatureRegistry:
    """Central registry governing all valid features in the platform."""

    def __init__(self):
        self._registry: Dict[str, FeatureRegistryEntry] = {}
        self._bootstrap_registry()

    def register(self, entry: FeatureRegistryEntry) -> None:
        self._registry[entry.name] = entry

    def get_feature(self, name: str) -> Optional[FeatureRegistryEntry]:
        return self._registry.get(name)

    def get_all_features(self) -> List[FeatureRegistryEntry]:
        return list(self._registry.values())

    def _bootstrap_registry(self) -> None:
        # 1. Temporal & Flux Features
        self.register(FeatureRegistryEntry(
            feature_id="F-TEMP-001",
            name="rise_time",
            description="Duration of the flare rise phase",
            scientific_meaning="Time taken from flare start to peak intensity",
            units="seconds",
            category="temporal",
            source_engine="characterization",
            source_variables=["rise_time"],
            dependencies=[],
            calculation_method="peak_time - start_time",
            normalization_strategy="minmax",
            allowed_range=(0.0, 10000.0),
            expected_distribution="lognormal",
            quality_rules={"min_value": 0.0},
            forecast_target_usage=["expected_duration"]
        ))
        self.register(FeatureRegistryEntry(
            feature_id="F-TEMP-002",
            name="decay_time",
            description="Duration of the flare decay phase",
            scientific_meaning="Time taken from flare peak to end of event",
            units="seconds",
            category="temporal",
            source_engine="characterization",
            source_variables=["decay_time"],
            dependencies=[],
            calculation_method="end_time - peak_time",
            normalization_strategy="minmax",
            allowed_range=(0.0, 30000.0),
            expected_distribution="lognormal",
            quality_rules={"min_value": 0.0},
            forecast_target_usage=["expected_duration"]
        ))
        self.register(FeatureRegistryEntry(
            feature_id="F-TEMP-003",
            name="duration",
            description="Total event duration",
            scientific_meaning="Total elapsed time of flare activity",
            units="seconds",
            category="temporal",
            source_engine="characterization",
            source_variables=["duration"],
            dependencies=[],
            calculation_method="end_time - start_time",
            normalization_strategy="minmax",
            allowed_range=(10.0, 40000.0),
            expected_distribution="lognormal",
            quality_rules={"min_value": 10.0},
            forecast_target_usage=["expected_duration"]
        ))
        self.register(FeatureRegistryEntry(
            feature_id="F-FLUX-001",
            name="peak_flux",
            description="Maximum observed flux level",
            scientific_meaning="Peak soft X-ray flux in W/m^2 equivalent",
            units="W/m^2",
            category="flux",
            source_engine="characterization",
            source_variables=["peak_flux"],
            dependencies=[],
            calculation_method="max(flux)",
            normalization_strategy="minmax",
            allowed_range=(1e-9, 1e-2),
            expected_distribution="lognormal",
            quality_rules={"min_value": 1e-9},
            forecast_target_usage=["goes_probability", "expected_peak_flux"]
        ))

        # 2. Thermal Features
        self.register(FeatureRegistryEntry(
            feature_id="F-THERM-001",
            name="peak_temperature",
            description="Peak flare plasma temperature",
            scientific_meaning="Maximum temperature reached by the emitting plasma",
            units="MK",
            category="thermal",
            source_engine="thermal",
            source_variables=["peak_temperature"],
            dependencies=[],
            calculation_method="spectral_fit_temperature",
            normalization_strategy="standard",
            allowed_range=(1.0, 100.0),
            expected_distribution="normal",
            quality_rules={"min_value": 1.0},
            forecast_target_usage=["goes_probability", "expected_peak_flux"]
        ))

        # 3. Derived Indices (Direct ML features)
        self.register(FeatureRegistryEntry(
            feature_id="F-IND-001",
            name="heating_index",
            description="Ratio of heating rate to cooling rate",
            scientific_meaning="Measures thermal energy input vs loss rate",
            units="dimensionless",
            category="indices",
            source_engine="indices",
            source_variables=["heating_rate", "cooling_rate"],
            dependencies=["heating_rate", "cooling_rate"],
            calculation_method="heating_rate / cooling_rate",
            normalization_strategy="standard",
            allowed_range=(0.0, 1000.0),
            expected_distribution="normal",
            quality_rules={"min_value": 0.0},
            forecast_target_usage=["goes_probability", "expected_duration"]
        ))
        self.register(FeatureRegistryEntry(
            feature_id="F-IND-002",
            name="thermal_dominance",
            description="Fractional thermal energy contribution",
            scientific_meaning="Thermal energy compared to total energy release",
            units="ratio",
            category="indices",
            source_engine="indices",
            source_variables=["thermal_energy", "total_energy"],
            dependencies=["thermal_energy", "total_energy"],
            calculation_method="thermal_energy / total_energy",
            normalization_strategy="none",
            allowed_range=(0.0, 1.0),
            expected_distribution="uniform",
            quality_rules={"min_value": 0.0, "max_value": 1.0},
            forecast_target_usage=["goes_probability"]
        ))


# Global singleton instance
feature_registry = FeatureRegistry()
