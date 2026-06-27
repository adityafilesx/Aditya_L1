# Neupert Effect Engine

The **Neupert Effect Engine** evaluates the physical relationship between the thermal plasma emission and the non-thermal electron acceleration. Under the standard solar flare model (the Neupert Effect), the cumulative energy deposited by accelerated electrons (traced by hard X-rays) is directly proportional to the accumulation of hot thermal plasma (traced by soft X-rays):

$$F_{SXR}(t) \propto \int_{t_0}^t F_{HXR}(t') dt'$$

## Core Capabilities
- **Temporal Offset**: Calculates the delay in seconds between the peak of hard X-rays (HEL1OS) and the peak of soft X-rays (SoLEXS). A positive offset (HXR peaking first) supports Neupert compliance.
- **Correlation & Compliance**: Computes the Pearson correlation coefficient between the cumulative time-integral of the HEL1OS flux and the SoLEXS flux profile.
- **Classification**: Categorizes the event's compliance into one of the following states:
  - `CONSISTENT`: Positive temporal offset and correlation coefficient $> 0.8$.
  - `PARTIAL`: Non-negative temporal offset and correlation coefficient $> 0.5$.
  - `ANOMALOUS`: Negative temporal offset or poor correlation.
  - `UNDETERMINED`: Insufficient overlapping data to compute correlation.

## Computation Status & Quality Metrics
- **`computation_status`**:
  - `GOOD`: Overlapping data window of at least 30 samples.
  - `DEGRADED`: Short overlap window ($< 30$ samples).
  - `INSUFFICIENT`: Bypassed if either SoLEXS or HEL1OS data is missing or if the event is single-instrument only.
- **`correlation_validity`**: Tracks confidence in the computed correlation coefficient.
