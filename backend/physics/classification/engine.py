"""
Flare Classification Engine.

Classifies the flare into GOES classes (A, B, C, M, X) based on peak soft
X-ray flux. Includes a configurable conversion factor since the simulator
uses arbitrary units.
"""

from __future__ import annotations

import math
from typing import Tuple

from backend.physics.models import FlareClassification, ClassificationQuality, GOESClass, ComputationStatus


class ClassificationEngine:
    """Classifies flares based on GOES equivalent flux."""

    VERSION = "1.0.0"

    # Conversion factor from simulated SoLEXS peak flux to GOES W/m^2
    # Simulated quiet sun is ~30, flares peak at ~100 to ~1000
    # Let's map 100 to C1 (10^-6), 1000 to X1 (10^-4)
    # Log-linear interpolation
    
    @staticmethod
    def _map_to_goes_flux(peak_solexs: float) -> float:
        if peak_solexs <= 30.0:
            return 1e-8 # A-class quiet

        # Simple empirical mapping for the simulator
        # C-class (~10^-6) at flux 100
        # M-class (~10^-5) at flux 300
        # X-class (~10^-4) at flux 1000
        # log10(flux) -> log10(goes_flux)
        
        # This is a very rough mapping purely for demonstration
        # goes_flux = 10^(log10(peak_solexs) * 2 - 10)
        # So flux 100 -> log10=2 -> goes = 10^(4-10) = 10^-6 (C1)
        # flux 316 -> log10=2.5 -> goes = 10^(5-10) = 10^-5 (M1)
        # flux 1000 -> log10=3 -> goes = 10^(6-10) = 10^-4 (X1)
        
        log_sol = math.log10(max(peak_solexs, 1.0))
        goes_exponent = log_sol * 2.0 - 10.0
        return 10.0 ** goes_exponent


    def classify(self, peak_soft_xray_flux: float, quality_metric: float = 1.0) -> Tuple[FlareClassification, ClassificationQuality]:
        """Classify flare based on peak soft X-ray flux."""

        if peak_soft_xray_flux <= 0:
             return (
                 FlareClassification(goes_class=GOESClass.UNKNOWN),
                 ClassificationQuality(computation_status=ComputationStatus.INSUFFICIENT, limiting_factor="No peak flux")
             )

        goes_flux = self._map_to_goes_flux(peak_soft_xray_flux)

        # Determine class
        if goes_flux < 1e-7:
            goes_class = GOESClass.A
            multiplier = goes_flux / 1e-8
        elif goes_flux < 1e-6:
            goes_class = GOESClass.B
            multiplier = goes_flux / 1e-7
        elif goes_flux < 1e-5:
            goes_class = GOESClass.C
            multiplier = goes_flux / 1e-6
        elif goes_flux < 1e-4:
            goes_class = GOESClass.M
            multiplier = goes_flux / 1e-5
        else:
            goes_class = GOESClass.X
            multiplier = goes_flux / 1e-4

        subclass = f"{goes_class.value}{multiplier:.1f}"

        # Quality
        status = ComputationStatus.GOOD if quality_metric > 0.5 else ComputationStatus.DEGRADED
        
        profile = FlareClassification(
            goes_class=goes_class,
            goes_subclass=subclass,
            peak_flux=goes_flux,
            classification_confidence=0.95 * quality_metric,
            classification_version=self.VERSION,
        )

        quality = ClassificationQuality(
            flux_measurement_quality=quality_metric,
            calibration_confidence=1.0, # Simulated perfect calibration
            computation_status=status,
            limiting_factor="" if status == ComputationStatus.GOOD else "Low quality input flux",
        )

        return profile, quality
