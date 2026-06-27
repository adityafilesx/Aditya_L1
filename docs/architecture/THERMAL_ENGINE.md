# Thermal Characterization Engine

The **Thermal Characterization Engine** computes the thermodynamic and thermal evolution of a solar flare from soft X-ray (SXR) fluxes. In this implementation, the primary input is from the **SoLEXS (Solar Low Energy X-ray Spectrometer)** payload data.

## Core Capabilities
- **Peak Temperature Calculation**: Estimates the peak temperature ($T_{peak}$ in Mega-Kelvin) by utilizing the Wien-approximation style soft-to-hard X-ray peak ratio ($F_{SoLEXS} / F_{HEL1OS}$).
- **Temperature Evolution**: Computes a continuous temperature profile $T(t)$ across the history buffer of the event.
- **Emission Measure ($EM$)**: Computes the plasma emission measure ($EM \approx \text{Flux} / T^2$), representing the quantity of emitting plasma, and stores it in log10 format (e.g., $10^{EM} \text{ cm}^{-3}$).
- **Heating & Cooling Rates**: Computes temporal derivatives of the temperature profile. Separate rates are derived for the positive derivative phase (heating rate in MK/s) and negative derivative phase (cooling rate in MK/s).
- **Thermal Energy**: Formulates the total thermal energy in ergs using a simplified coronal model:
  $$E_{th} = 3 k_B T \sqrt{EM} \sqrt{V}$$
  where $V$ is a representative coronal loop volume ($10^{27} \text{ cm}^3$).

## Computation Status & Quality Metrics
The engine produces a `ThermalQuality` object reflecting the computation's mathematical validity:
- **`data_coverage`**: A fraction representing the presence of required time-series data.
- **`computation_status`**:
  - `GOOD`: Sufficient history samples ($\ge 30$) to run differential cooling/heating rates.
  - `DEGRADED`: Limited history samples ($10 \le N < 30$), leading to reduced confidence in derivative curves.
  - `INSUFFICIENT`: Fewer than 10 samples; calculations are bypassed, returning default zeroes.
- **`limiting_factor`**: Contextual message explaining a degraded or insufficient status.
