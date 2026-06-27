# Spectral Decomposition Engine

The **Spectral Decomposition Engine** performs multi-component analysis of the observed X-ray spectrum, modeling it as a combination of a thermal plasma component and a non-thermal power-law component.

## Core Capabilities
- **Thermal & Non-Thermal Fraction**: Decomposes the observed emission into relative fractional contributions (0.0 to 1.0) based on the ratio of soft X-ray (SoLEXS) to hard X-ray (HEL1OS) peak fluxes.
- **Power-Law Index ($\gamma$)**: Approximates the spectral index $\gamma$ of the hard X-ray spectrum by analyzing the log-log slope of the HEL1OS count rate. A smaller index indicates a "harder" spectrum with a greater proportion of high-energy photons.
- **Energy Cutoffs**: Estimates the low-energy thermal cutoff (keV) and high-energy non-thermal cutoff (keV) to establish bounds for future model calculations.
- **Goodness of Fit ($GoF$)**: Computes a fit validation metric based on the residual between the fractional components and unity ($1.0 - \text{residual} \times 10$).

## Computation Status & Quality Metrics
The engine produces a `SpectralQuality` object:
- **`fit_residual_norm`**: Represents the deviation of the multi-component decomposition from physical conservation.
- **`computation_status`**:
  - `GOOD`: Clean, synchronized dual-instrument data with sufficient sample counts ($\ge 10$ samples per instrument).
  - `DEGRADED`: Limited spectral coverage ($< 10$ samples per instrument).
  - `INSUFFICIENT`: Fails when either instrument has fewer than 3 samples.
