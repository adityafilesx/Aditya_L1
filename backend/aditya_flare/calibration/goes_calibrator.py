import yaml
import numpy as np
from pathlib import Path
from backend.aditya_flare.calibration.calibration_utils import flux_to_goes_class_string

class GoesCalibrator:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent / "calibration_config.yaml"
        else:
            config_path = Path(config_path)

        self.slope = 1.05
        self.intercept = -9.5
        
        if config_path.exists():
            with open(config_path, "r") as f:
                data = yaml.safe_load(f) or {}
                scale = data.get("scale", {})
                self.slope = scale.get("slope", 1.05)
                self.intercept = scale.get("intercept", -9.5)

    def counts_to_flux(self, cps: float) -> float:
        """
        Approximates GOES flux (W/m^2) from SoLEXS counts/sec.
        Uses a log-log linear scaling: log10(Flux) = slope * log10(cps) + intercept
        """
        if cps <= 0 or np.isnan(cps):
            return 1e-9 # Background minimal A-class

        log_cps = np.log10(cps)
        log_flux = self.slope * log_cps + self.intercept
        return 10 ** log_flux

    def flux_to_class(self, flux: float) -> str:
        """
        Converts flux directly to GOES Class string.
        """
        return flux_to_goes_class_string(flux)
        
    def cps_to_class(self, cps: float) -> str:
        flux = self.counts_to_flux(cps)
        return self.flux_to_class(flux)
