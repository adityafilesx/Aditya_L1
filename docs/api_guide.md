# API Guide

## `aditya_flare.calibration.GoesCalibrator`

The `GoesCalibrator` handles the conversion of instrument counts into GOES flux values.

- `counts_to_flux(cps: float) -> float`: Returns the estimated GOES 1-8A flux (W/m²).
- `flux_to_class(flux: float) -> str`: Returns the GOES class string (e.g., 'M3.2').
- `cps_to_class(cps: float) -> str`: Directly converts counts/sec to a GOES class string.

## `aditya_flare.evaluation.BenchmarkSuite`

Facilitates multi-model performance comparisons.

- `add_model(name: str, y_true: np.ndarray, y_prob: np.ndarray)`: Adds model predictions to the suite.
- `run_benchmarks() -> dict`: Returns a dictionary of computed metrics across all registered models.

## `aditya_flare.config.config_loader`

Centralized configuration loader.

- `config`: Global instantiated `Config` object loaded from `settings.yaml`.
