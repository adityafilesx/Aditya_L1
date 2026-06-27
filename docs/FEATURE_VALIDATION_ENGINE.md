# Feature Validation Engine

The Runtime Feature Validation Engine executes automatically on every extraction tick to ensure variables satisfy technical and physical constraints before store serialization.

## Validation Metrics
- **Missing / NaN / Inf Checks**: Triggers immediately on invalid numbers.
- **Scientific Bounding**: Validates values sit within the allowed ranges defined in the Registry.
- **Consistency Checks**: Ensures temporal sequences are logical (e.g. `rise_time` + `decay_time` matches `duration`).

## Validation Outputs
Each feature validation returns a status:
1. `VALID`: Satisfies all bounds and rules.
2. `WARNING`: Unregistered feature metadata.
3. `DEGRADED`: Value exceeds bounds slightly but remains technically processable.
4. `INVALID`: Crucial NaN, Infinite, or negative violations. Invalid vectors are rejected from the store.
