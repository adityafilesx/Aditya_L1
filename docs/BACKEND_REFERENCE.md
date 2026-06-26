# Backend Reference Manual — Aditya-L1 Platform

This document describes the design, implementation, and interfaces of the backend systems for the Aditya-L1 Space Weather Intelligence Platform.

---

## 1. Subsystem Implementation Details

### 1.1 Telemetry Ingestion & Calibration
*   **Module:** `aditya_flare/processing/` and `aditya_flare/calibration/`
*   **Ingestion:** Reads raw datasets (Parquet/CSV) and aligns instrument timelines (SoLEXS, HEL1OS, external GOES channels) to a 1-minute cadence using forward-fill interpolation:
    ```python
    df_resampled = df.resample('1min').mean().ffill()
    ```
*   **Calibration:** Converts instrument counts to physical flux values ($W/m^2$):
    ```python
    flux = counts * calibration_factor + calibration_offset
    ```

### 1.2 Physics Engine
*   **Module:** `physics_engine/`
*   **Neupert Effect:** Calculates the correlation between the hard X-ray flux ($F_{hard}$) and the soft X-ray derivative ($\frac{dF_{soft}}{dt}$):
    $$ r = \frac{\sum (F_{hard} - \bar{F}_{hard})(\frac{dF_{soft}}{dt} - \bar{\frac{dF_{soft}}{dt}})}{\sqrt{\sum (F_{hard} - \bar{F}_{hard})^2 \sum (\frac{dF_{soft}}{dt} - \bar{\frac{dF_{soft}}{dt}})^2}} $$
*   **Wavelet Scalograms:** Uses Continuous Wavelet Transforms (CWT) with Complex Morlet wavelets to extract dominant oscillation frequencies:
    ```python
    scales = np.arange(1, 128)
    coefficients, frequencies = pywt.cwt(flux_signal, scales, 'cmor1.5-1.0')
    ```
*   **Spectral Analytics (PSD):** Uses Fast Fourier Transforms (FFT) to extract spectral peaks and assess spectral flatness:
    ```python
    frequencies, psd = scipy.signal.welch(flux_signal, fs=1/60)
    flatness = np.exp(np.mean(np.log(psd))) / np.mean(psd)
    ```

### 1.3 AI & Forecasting Engine
*   **Module:** `aditya_flare/ai_engine/`
*   **Nowcast Models:** Uses gradient-boosted decision trees (XGBoost/LightGBM) to evaluate short-range flare risks.
*   **Sequence Forecasting Models:**
    *   *TCN:* Temporal Convolutional Network with dilated causal convolutional layers for long-term sequence forecasting.
    *   *Transformer:* Multi-head self-attention network for sequence forecasting.
*   **Explainability:** Integrates SHAP values to identify feature impacts for model forecasts:
    ```python
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(features)
    ```

### 1.4 Decision & Mission Operations Engine
*   **Module:** `aditya_flare/decision/`
*   **State Machine:** Implements a deterministic state engine to transition spacecraft alert states:
    ```
    NOMINAL -> WATCH -> ALERT -> DECAY -> RECOVERY
    ```
*   **Recommendation Engine:** Generates plain-text command actions based on the current alert state, active warnings, and telemetry health.
*   **Drift Monitor:** Uses Kolmogorov-Smirnov tests to identify sensor drift by comparing live telemetry against baseline distributions:
    ```python
    ks_stat, p_val = scipy.stats.ks_2samp(live_window, baseline_window)
    ```

### 1.5 Multi-Modal Fusion, Digital Twin, & Knowledge Graph
*   **Module:** `aditya_flare/multi_modal/`
*   **Fusion Network:** Uses cross-modal cross-attention layers to map multi-instrument telemetry features.
*   **Digital Twin State Tracker:** Evaluates similarity scores and complexity metrics across solar active region templates.
*   **Knowledge Graph:** Constructs a relational network mapping connections between active regions, solar events, and alert triggers.

---

## 2. Infrastructure & Operations

### 2.1 Centralized Logging System
*   **Implementation:** Configures rotating file loggers to write operational logs to `/data/logs/`:
    *   `inference.log`: Logs model inference inputs, outputs, and latencies.
    *   `state_transitions.log`: Logs spacecraft state transitions and trigger rules.
    *   `calibration_drift.log`: Logs drift metrics and KS-statistic warnings.

### 2.2 Validation & Testing Suites
*   **Implementation:** Runs automated unit tests via `pytest` to verify calibration accuracy, resampler alignment, and physics calculations.
*   **Test Modules:**
    *   `tests/test_calibration.py`: Verifies count-to-flux transformations.
    *   `tests/test_data_merger.py`: Verifies resampler interpolation and data alignment.
    *   `tests/test_physics_engine.py`: Verifies Neupert correlation, wavelets, and PSD calculations.
    *   `tests/test_explainability.py`: Verifies SHAP explainability runs without errors.
