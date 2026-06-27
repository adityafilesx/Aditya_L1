# Detector Parameter Configuration

To allow scientific tuning without modifying backend source code, the **Nowcasting Engine** consolidates all detector parameters, buffers, smoothing coefficients, and thresholds into a central configuration schema.

## Configuration Structure
The configuration is defined in `backend/nowcasting/config.py` using Pydantic, and loaded from `backend/nowcasting/config.yaml` at startup.

### SoLEXS Detector Parameters
- **`buffer_size`**: Length of the sliding observation buffer (default: `120` samples).
- **`ema_alpha`**: Smoothing coefficient ($0 < \alpha \le 1$) for the background estimation (default: `0.02`).
- **`monitoring_threshold`**: Flux-to-background ratio above which the system starts tracking (default: `1.2`).
- **`rising_threshold`**: Flux-to-background ratio marking the initiation of a flare event (default: `1.5`).
- **`active_threshold`**: Flux-to-background ratio representing peak flare status (default: `2.0`).
- **`decay_drop_fraction`**: Fractional drop below peak flux triggering transition to `DECAY` state (default: `0.2`).
- **`ended_threshold`**: Flux-to-background ratio indicating return to baseline quiet sun (default: `1.3`).

### HEL1OS Detector Parameters
- **`buffer_size`**: Length of the sliding observation buffer (default: `60` samples).
- **`spike_sigma`**: Number of standard deviations above baseline to register a hard X-ray spike (default: `3.0`).
- **`rising_persistence`**: Number of consecutive samples above threshold to declare a burst event (default: `2`).
- **`decay_sigma`**: Standard deviation threshold to transition to `DECAY` state (default: `2.0`).
- **`ended_sigma`**: Standard deviation threshold to declare the burst has ended (default: `1.0`).

### Association Parameters
- **`temporal_window_s`**: Maximum time window (seconds) allowed between SoLEXS and HEL1OS triggers to associate them as a single event (default: `120.0`).
- **`neupert_max_delay_s`**: Maximum allowed delay (seconds) of the HEL1OS peak preceding the SoLEXS peak (default: `60.0`).
- **`association_threshold`**: Threshold to qualify events as associated (default: `0.6`).
