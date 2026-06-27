# Non-Thermal Characterization Engine

The **Non-Thermal Characterization Engine** isolates and characterizes the high-energy, particle-acceleration processes occurring in the solar atmosphere. It operates primarily on counts and fluxes from the **HEL1OS (High Energy L1 Orbiting Spectrometer)** payload.

## Core Capabilities
- **Peak Electron Energy**: Computes the highest energy ($E_{peak}$ in keV) attained by accelerated electrons during the impulsive phase.
- **Burst Energy**: Computes the integrated counts above the background level during the non-thermal event.
- **Hard X-Ray Energy**: Quantifies the total radiated non-thermal energy in ergs:
  $$E_{HXR} = \text{Burst Energy} \times 1.6 \times 10^{-12} \text{ ergs/keV}$$
- **Electron Flux**: Computes the rate of electron emission (electrons/s/cm²) based on peak counts divided by the burst duration.
- **Acceleration Duration**: Traces the time interval (seconds) from the detected start of the hard X-ray burst to its peak intensity.
- **Impulsive Phase Duration**: Tracks the total length of time that hard X-ray emission remains significantly above the pre-flare background level ($\ge 2\times$ background).

## Computation Status & Quality Metrics
The engine produces a standard quality model with the following behavior:
- **`computation_status`**:
  - `GOOD`: Clear burst detected with well-defined start and end points.
  - `DEGRADED`: A burst is present, but either the signal-to-noise ratio is low or the impulsive phase is extremely short ($< 3$ seconds).
  - `INSUFFICIENT`: Bypassed when there are fewer than 3 samples or no HEL1OS event is associated.
