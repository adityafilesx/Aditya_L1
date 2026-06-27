"""
Indices Engine.

Computes derived, dimensionless indices from the various physics profiles.
These indices are explicitly designed as high-value, scale-invariant features
for downstream machine learning models (Forecasting and Feature Engineering).
"""

from __future__ import annotations

import math

from backend.physics.models import (
    PhysicsDerivedIndices,
    ThermalProfile,
    NonThermalProfile,
    SpectralProfile,
    NeupertProfile,
    EventCharacterization,
)


class IndicesEngine:
    """Computes derived physics indices for ML feature engineering."""

    VERSION = "1.0.0"

    def compute(
        self,
        thermal: ThermalProfile,
        nonthermal: NonThermalProfile,
        spectral: SpectralProfile,
        neupert: NeupertProfile,
        char: EventCharacterization,
    ) -> PhysicsDerivedIndices:

        # 1. Heating Index (heating_rate / cooling_rate)
        # > 1 means heating dominates, < 1 means cooling dominates
        heating_index = 0.0
        if thermal.cooling_rate > 0:
            heating_index = thermal.heating_rate / thermal.cooling_rate
        elif thermal.heating_rate > 0:
            heating_index = 99.0  # arbitrary high value for heating with zero cooling

        # 2. Cooling Index (decay_time / rise_time)
        # Characterizes the asymmetry of the flare profile
        cooling_index = 0.0
        if char.rise_time > 0:
            cooling_index = char.decay_time / char.rise_time

        # 3. Energy Release Index (log10 total energy)
        # Scale-invariant measure of overall event magnitude
        total_energy = thermal.thermal_energy + nonthermal.hard_xray_energy
        energy_release_index = 0.0
        if total_energy > 0:
            energy_release_index = math.log10(max(total_energy, 1.0))

        # 4. Thermal Dominance (thermal / total energy)
        # 0 = purely non-thermal, 1 = purely thermal
        thermal_dominance = 0.0
        if total_energy > 0:
            thermal_dominance = thermal.thermal_energy / total_energy

        # 5. Neupert Compliance (score * consistency)
        # 0 = violates Neupert, 1 = perfectly follows Neupert
        neupert_compliance = neupert.neupert_score * neupert.neupert_consistency

        # 6. Spectral Hardness (1 / power_law_index)
        # Smaller power law index = "harder" spectrum = higher hardness index
        spectral_hardness = 0.0
        if spectral.power_law_index > 0:
            spectral_hardness = 1.0 / spectral.power_law_index

        # 7. Impulsiveness Index (peak / mean_flux)
        # Mean flux = integrated_flux / duration
        impulsiveness = 0.0
        if char.duration > 0 and char.integrated_flux > 0:
            mean_flux = char.integrated_flux / char.duration
            impulsiveness = char.peak_flux / mean_flux

        return PhysicsDerivedIndices(
            heating_index=round(heating_index, 4),
            cooling_index=round(cooling_index, 4),
            energy_release_index=round(energy_release_index, 4),
            thermal_dominance=round(thermal_dominance, 4),
            neupert_compliance=round(neupert_compliance, 4),
            spectral_hardness=round(spectral_hardness, 4),
            impulsiveness_index=round(impulsiveness, 4),
        )
