# 07. AI Model Documentation

This document describes the design, training parameters, inference pipelines, and calibration steps of the machine learning models.

---

## 📈 Nowcasting XGBoost Model

### Architecture
A Gradient Boosted Decision Tree (GBDT) classifier configured for instant flare state classification. It is stored as a compiled JSON file: `backend/data/models/xgboost_nowcast.json`.

### Inputs
*   `goes_flux_instant`: Instant long-band GOES X-ray flux.
*   `goes_flux_derivative`: Instant derivative of the flux curve.
*   `solexs_count_rate`: Soft X-ray counts from SDD2.
*   `helios_count_rate`: Hard X-ray counts from HEL1OS.

### Outputs
Probability distribution over 4 classes: `Quiet`, `Rise`, `Peak`, `Decay`.

---

## 🕒 Temporal Convolutional Network (TCN)

### Architecture
Dilated 1D convolutions with causal padding, residual connections, and weight normalization. Designed to extract short-term temporal dependencies from count rate sequences.

### Inputs
A timeseries history of shape `(batch_size, sequence_length, features)` where:
*   `sequence_length` = 60 steps (1 minute of telemetry at 1Hz).
*   `features` = 6 physical features.

### Outputs
Feature vector fed into the Hybrid Ensemble.

---

## 🌌 Temporal Transformer Forecaster

### Architecture
Standard multi-head self-attention encoder layers with sinusoidal positional encodings. Designed to capture long-range correlation and global solar patterns (such as multi-hour active region decay phases).

### Training Configuration
*   **Loss Function**: Weighted binary cross-entropy (due to class imbalance of X/M flares vs quiet days).
*   **Optimizer**: AdamW.
*   **Learning Rate Schedule**: Cosine annealing.

---

## 🤝 Hybrid Ensemble

### Architecture
An ensemble pipeline combining the latent states of the TCN and the Transformer, topped with a logistic regression meta-classifier.
Stored at: `backend/data/models/ensemble_forecaster.pkl`.

```
                    +-----------------------+
                    | Raw Telemetry History |
                    +-----------------------+
                                |
                   +------------+------------+
                   |                         |
                   v                         v
         +-------------------+     +--------------------+
         |   TCN Feature     |     |   Transformer      |
         |    Extractor      |     |  Attention Block   |
         +-------------------+     +--------------------+
                   |                         |
                   +------------+------------+
                                |
                                v
                    +-----------------------+
                    |   Meta-Classifier     |
                    | (Logistic Regression) |
                    +-----------------------+
                                |
                                v
                      [ Flare Probability ]
```

---

## 🎯 Conformal Prediction & Calibration

To ensure reliability, the raw ensemble output probability is calibrated using **conformal prediction intervals**. This guarantees that the true outcome falls within the predicted confidence band with a user-specified probability (e.g. 90%).

### Calibration Method
Calibrated using a calibration dataset of historical M/X class flares:
1.  **Non-conformity Score**: Computes the absolute discrepancy between the model probability and actual outcome.
2.  **Quantile Computation**: Computes the $(1-\alpha)$ quantile of these scores.
3.  **Confidence Bounds**: The backend computes a lower and upper confidence bound exported alongside the raw forecast prediction.
