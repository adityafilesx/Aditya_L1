# 18. Scientific Glossary

This glossary defines the astrophysical and system engineering terms utilized throughout the Aditya-L1 Space Weather Intelligence Platform.

---

## 🔬 Scientific Terms

### 1. Neupert Effect
The empirical observation that the soft X-ray (SXR) emission from a solar flare is roughly proportional to the time integral of the hard X-ray (HXR) emission. Physically, this suggests that the non-thermal electron beam acceleration (traced by HXR) acts as the primary energy source heating the thermal flare plasma (traced by SXR).

$$F_{SXR}(t) \propto \int_{t_0}^t F_{HXR}(\tau) d\tau$$

### 2. Differential Emission Measure (DEM)
A physical property representing the amount of solar plasma emitting radiation as a function of temperature. It is calculated from flux ratios to estimate the thermal structure of active regions.

### 3. Wavelet Transform
A signal processing technique that decomposes a 1D timeseries into frequency components while preserving temporal localization. The platform uses Continuous Wavelet Transform (CWT) to identify pre-flare oscillation patterns in count rates.

### 4. Power Spectral Density (PSD)
A measure of the signal's power content versus frequency. Calculated over sensor count streams to detect active region oscillations.

### 5. Geostationary Operational Environmental Satellites (GOES)
A series of weather satellites operated by NOAA. The platform uses the GOES X-ray Sensor (XRS) long-band (0.1–0.8 nm) and short-band (0.05–0.4 nm) flux data as baseline telemetry inputs.

### 6. Solar Low Energy X-ray Spectrometer (SoLEXS)
A payload on India's Aditya-L1 spacecraft that measures soft X-rays (1–30 keV) to observe active region heating profiles.

### 7. High Energy L1 Orbiting X-ray Spectrometer (HEL1OS)
An instrument on Aditya-L1 designed to capture hard X-rays (10–150 keV) for tracking the particle acceleration phase of solar flares.

### 8. Nowcasting
The instantaneous detection and characterization of ongoing solar events (such as classifying if a flare is currently rising, peaking, or decaying).

### 9. Forecasting
The prediction of future solar events (e.g. estimating the probability of a flare occurring over a future 15m to 6h window).

### 10. Conformal Prediction
A statistical framework that supplements machine learning point predictions with exact, mathematically guaranteed confidence intervals.
