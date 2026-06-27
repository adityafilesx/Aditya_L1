# SoLEXS Detector

## Overview
The `SolexsDetector` is a highly configurable, sliding-window based real-time flare detector optimized for the Aditya-L1 SoLEXS payload (Solar Low Energy X-ray Spectrometer). Its primary purpose is to identify gradual thermal X-ray rises typical of solar flare precursors and main phases in the 1-30 keV range.

## Mechanism
Unlike impulsive burst detectors, the SoLEXS Detector relies on an adaptive Exponential Moving Average (EMA) and derivative tracking to identify long-duration flux increases. 

1. **Background Modeling**: It maintains an adaptive background model that continuously updates during nominal solar conditions.
2. **Derivative Tracking**: It calculates the short-term derivative of the soft X-ray flux to detect the onset of a thermal rise.
3. **Thresholds**: 
   - `pre_flare_threshold`: Triggers the `PRE_FLARE` state when the flux begins to rise steadily above the EMA but hasn't reached the main flare threshold.
   - `flare_threshold`: Triggers the `ACTIVE` state when the flux unequivocally indicates a flare event.
4. **State Machine**: The detector transitions through a strict state machine: `NOMINAL` → `PRE_FLARE` → `ACTIVE` → `PEAK` → `DECAY` → `NOMINAL`.

## Configuration Parameters
The detector is highly configurable to allow for tuning based on actual in-flight sensor performance:
- `window_size`: The size of the sliding observation buffer (default: 300 seconds).
- `ema_alpha`: The smoothing factor for the background EMA (default: 0.05).
- `pre_flare_sigma`: The standard deviation threshold above background to trigger a pre-flare warning.
- `flare_sigma`: The standard deviation threshold above background to trigger a full flare state.
- `decay_threshold`: The percentage drop from the peak flux required to enter the `DECAY` state.

## Output
The detector yields a `DetectorEvent` object when a flare is identified. This event includes:
- `instrument`: 'SOLEXS'
- `start_time`: Precise onset timestamp.
- `peak_time`: Timestamp of maximum flux (if reached).
- `peak_flux`: Maximum recorded flux.
- `confidence`: Calculated dynamically based on the sustained derivative and sigma deviation.

## Independence
The SoLEXS detector operates completely independently of the HEL1OS detector, fulfilling the requirement for multi-instrument independent observation pipelines before association.
