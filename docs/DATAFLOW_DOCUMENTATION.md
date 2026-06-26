# Data Flow Documentation — Aditya-L1 Space Weather Platform

This document describes the end-to-end data pipeline from raw telemetry files to operational mission decisions.

---

## 1. End-to-End Data Pipeline

Below is the structured data flow diagram:

```mermaid
graph TD
    %% Source
    RawTelemetry[Raw Telemetry Streams: Parquet / CSV] --> Ingest[aditya_flare.processing]
    
    %% Ingest & Cleanse
    Ingest --> Resample[1-Minute Cadence Resampler]
    Resample --> Interpolate[Gap Interpolator]
    Interpolate --> CleanedData[Cleaned Data Frame]
    
    %% Calibration
    CleanedData --> Calib[Calibration Engine: fit_conformal_calibration]
    Calib --> CalibData[Calibrated Flux Values W/m²]
    
    %% Feature Processing Splits
    CalibData --> FeatureExtract[Feature Engineering Matrix]
    
    %% Engine Compute Paths
    subgraph Physics Engine Computations
        FeatureExtract --> Neupert[Neupert Derivative dF/dt]
        FeatureExtract --> PSD[Power Spectral Density via FFT]
        FeatureExtract --> Wavelet[Wavelet Transforms]
    end
    
    subgraph AI/ML Forecasting Computations
        FeatureExtract --> XGBoost[XGBoost Classifier]
        FeatureExtract --> TCN[Temporal Conv Net]
        FeatureExtract --> Transformer[Transformer Attention]
    end
    
    %% Assembly & Diagnostics
    Neupert --> DiagnosticFusion[Diagnostic Feature Ingest]
    PSD --> DiagnosticFusion
    Wavelet --> DiagnosticFusion
    
    XGBoost --> Ensemble[Ensemble Forecast Consensus]
    TCN --> Ensemble
    Transformer --> Ensemble
    
    %% Decision Layer
    DiagnosticFusion --> Decision[Decision Engine]
    Ensemble --> Decision
    
    Decision --> StateMachine[Operational State Machine]
    Decision --> Alerts[Alert Manager Alert Generation]
    
    %% Output DTO
    StateMachine --> JSON[JSON API Contract Outputs]
    Alerts --> JSON
```

---

## 2. Pipeline Phase Execution

1.  **Ingestion & Alignment:**
    *   Reads daily parquet files and resamples to a 1-minute cadence.
    *   Aligns external reference streams (e.g. GOES XRS) with spacecraft payload measurements.
2.  **Physical Calibration:**
    *   Applies counts-to-flux calibration vectors to translate photon counts/sec into physical Solar Flare class ranges ($B, C, M, X$).
3.  **Compute Splitting:**
    *   **Physics Branch:** Calculates derivative curves and power spectra to map thermal changes.
    *   **AI Branch:** Assembles sequence vectors to generate probabilistic flare onset forecasts.
4.  **Operational Triggers:**
    *   Takes probability levels and physical flags to drive the deterministic spacecraft state machine.
    *   Dispatches actions (such as triggering spacecraft high-cadence burst acquisition) based on the calculated alert states.
