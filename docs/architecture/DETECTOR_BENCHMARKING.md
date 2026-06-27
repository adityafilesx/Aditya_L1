# Detector Performance & Latency Benchmarking

To ensure the forecasting workstation remains responsive under high telemetry loads, the **Nowcasting Engine** tracks real-time detector performance, stability, and latency metrics.

## Performance Tracking Metrics
Each detector (SoLEXS and HEL1OS) is wrapped by a `DetectorBenchmark` instance that records:
- **`detection_latency_avg`**: Average processing latency in milliseconds per observation tick.
- **`false_trigger_rate`**: Fraction of triggers that do not resolve into full, unified events.
- **`stability`**: Operational status indicator ($1.0$ for stable, $0.0$ for unstable). The detector is marked unstable if it encounters more than 3 consecutive errors.
- **`avg_confidence`**: Mean confidence value of completed events.
- **`total_events`**: Total number of events successfully captured.
- **`missed_detections`**: Number of event signatures that failed to trigger the thresholds.

## Real-Time Health Diagnostics
In addition to benchmarks, the backend tracks system health parameters:
- **`DetectorHealthSnapshot`**: Reports GPU/CPU memory utilisation, active threads, and processing frequency (frames per second).
- These parameters are broadcasted over the WebSocket interface (`NowcastState`) and rendered in the **Workstation Diagnostics Panel**.
