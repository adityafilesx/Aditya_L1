# HEL1OS Detector

## Overview
The `HeliosDetector` is tailored for the Aditya-L1 HEL1OS payload (High Energy L1 Orbiting X-ray Spectrometer). Its objective is the immediate identification of impulsive hard X-ray bursts that correspond to particle acceleration and bremsstrahlung emission in the early impulsive phase of a solar flare (10-150 keV).

## Mechanism
Hard X-ray emission is highly impulsive and short-lived. Therefore, the HEL1OS detector uses a shorter, faster sliding window and a strict dynamic sigma threshold rather than the gradual EMA approach used by SoLEXS.

1. **Short Sliding Window**: Maintains a highly responsive background buffer (e.g., 60 seconds).
2. **Sigma Thresholding**: Continuously calculates the standard deviation (sigma) of the background buffer. If a new observation exceeds the background mean by `N` sigma (where `N` is configurable, typically 4-5), an impulsive event is triggered immediately.
3. **Neupert Validation Readiness**: While the HEL1OS detector itself does not check the Neupert effect (as it operates independently), its output format is designed to allow the `EventAssociator` to easily align the impulsive HEL1OS spike with the derivative of the SoLEXS thermal rise.
4. **State Machine**: The state transitions are extremely rapid: `NOMINAL` → `ACTIVE` (impulsive spike) → `NOMINAL`. Pre-flare states are generally not applicable to hard X-ray emission.

## Configuration Parameters
- `window_size`: Short sliding buffer (default: 60 seconds).
- `sigma_threshold`: The standard deviation multiplier required to trigger an event (default: 4.5).
- `minimum_duration`: To filter out single-photon cosmic ray hits, a spike must be sustained for a minimum number of seconds (default: 2 seconds).

## Output
The `DetectorEvent` produced by HEL1OS is concise:
- `instrument`: 'HEL1OS'
- `start_time`: Timestamp of the impulsive spike.
- `peak_flux`: The maximum hard X-ray count rate.
- `confidence`: Very high if sustained, lower if it barely meets the minimum duration.
