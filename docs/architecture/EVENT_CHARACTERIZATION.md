# Event Temporal Characterization Engine

The **Event Temporal Characterization Engine** computes timing, durations, rise/decay characteristics, and signal quality metrics for each flare event.

## Core Capabilities
- **Rise & Decay Time**: Calculates the duration of the rise phase ($t_{peak} - t_{start}$) and decay phase ($t_{end} - t_{peak}$) in seconds.
- **Total Duration**: Measures the entire active lifecycle of the flare event.
- **Maximum Flux Derivative**: Identifies the maximum rate of flux increase ($d\text{Flux}/dt$), which marks the peak energy release rate.
- **Integrated Flux**: Computes the area under the flux curve above the pre-flare background level.
- **Signal-to-Noise Ratio (SNR)**: Computes the ratio of peak flux to the pre-flare quiet sun background level, serving as a measure of event detection significance.

## Computation Status & Quality Metrics
- **`computation_status`**:
  - `GOOD`: Valid temporal bounds ($t_{start} < t_{peak} < t_{end}$) and positive duration.
  - `DEGRADED`: Timing bounds are incomplete or duration calculations are anomalous.
  - `INSUFFICIENT`: Bypassed if timestamps are completely missing.
- **`snr_adequacy`**: Scaled representation of the signal-to-noise ratio ($SNR / 10.0$ capped at $1.0$).
