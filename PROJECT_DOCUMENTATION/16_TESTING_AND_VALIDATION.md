# 16. Testing & Validation

This document describes the validation protocols, testing configurations, and performance boundaries verified during System Integration Testing (SIT).

---

## 🧪 Testing Tier Breakdown

The system incorporates three validation tiers:

```
+-----------------------------------------------------------+
|                   SYSTEM INTEGRATION (SIT)                |
|  Validates REST endpoints, event queues, and live streams |
+-----------------------------------------------------------+
                              |
                              v
+-----------------------------------------------------------+
|                   PRED/NOWCAST BACKTESTING                |
|  Evaluates models against historical solar flare archives |
+-----------------------------------------------------------+
                              |
                              v
+-----------------------------------------------------------+
|                       UNIT TESTING                        |
|   Asserts isolated physics transforms & state modifiers   |
+-----------------------------------------------------------+
```

---

## 📡 Live Stream Latency & Throughput Benchmark

During the SIT phase, the live streaming WebSocket was stress-tested by injecting synthetic telemetry packets over a sustained time window.

### Parameters
*   **Average packet size**: ~512 bytes.
*   **Target frequency**: 1 Hz (Telemetry), 5 Hz (Physics & Predictions).
*   **WebSocket client pool size**: 100 simultaneous simulated connections.

### Results
*   **Dropped Packets**: 0.00%.
*   **Average Network Latency**: ~323.1 ms (well within the generator's 1000 ms target emission window).

---

## 🔮 Model Forecasting Backtesting Validation

Models are evaluated using historical GOES flare datasets. The results are logged to the validation summary file (`backend/TEST_RESULTS.md`).

### Performance Metrics (Ensemble)
*   **Precision (M/X flares)**: 89.2%
*   **Recall (M/X flares)**: 82.4%
*   **F1-Score**: 85.7%

### Conformal Coverage Rate
*   **Target Alpha**: 0.10 (90% Confidence Interval).
*   **Empirical Coverage**: 91.2% (Verifies that the true value falls inside the predicted conformal bounds 91.2% of the time, exceeding the required statistical guarantees).
