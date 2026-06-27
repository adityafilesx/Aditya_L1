"""
Plasma State Engine.

Computes fundamental plasma parameters (density, pressure, thermal content)
from the thermal and non-thermal properties of the flare.
"""

from __future__ import annotations

import math

from backend.physics.models import PlasmaProfile, ThermalProfile, NonThermalProfile, PlasmaState

K_B = 1.38e-16       # Boltzmann constant (erg/K)
MK_TO_K = 1.0e6      # mega-Kelvin to Kelvin
LOOP_VOLUME = 1e27    # cm³ — representative coronal loop volume


class PlasmaEngine:
    """Computes the plasma state from thermal parameters."""

    VERSION = "1.0.0"

    def characterize(
        self,
        thermal: ThermalProfile,
        nonthermal: NonThermalProfile,
    ) -> PlasmaProfile:

        if thermal.peak_temperature <= 0 or thermal.emission_measure <= 0:
            return PlasmaProfile(plasma_state=PlasmaState.UNKNOWN)

        # Plasma density: n_e ~ sqrt(EM / V)
        # EM is stored in log10(cm^-3) in ThermalProfile
        em_linear = 10.0 ** thermal.emission_measure
        density = math.sqrt(em_linear / LOOP_VOLUME)

        # Plasma pressure: p = 2 n_e k_B T (assuming n_e ~ n_i)
        temp_k = thermal.peak_temperature * MK_TO_K
        pressure = 2.0 * density * K_B * temp_k

        # Thermal content: U = 3 n_e k_B T V (approximate)
        thermal_content = 3.0 * density * K_B * temp_k * LOOP_VOLUME

        # Plasma state inference
        state = PlasmaState.QUIET
        if thermal.heating_rate > thermal.cooling_rate and thermal.heating_rate > 0:
            state = PlasmaState.HEATING
        elif thermal.cooling_rate > thermal.heating_rate and thermal.cooling_rate > 0:
            state = PlasmaState.COOLING
        elif thermal.peak_temperature > 10.0:
            state = PlasmaState.PEAK

        # Magnetic field placeholder (typically from vector magnetograms, which we don't have)
        magnetic_placeholder = 100.0  # Gauss

        return PlasmaProfile(
            density=density,
            pressure=pressure,
            energy=thermal_content + nonthermal.hard_xray_energy,
            thermal_content=thermal_content,
            magnetic_placeholder=magnetic_placeholder,
            plasma_state=state,
        )
