# Scientific Observation Validation & Preprocessing Engine

## Overview
The Observation Engine is the foundational telemetry processing layer of the Aditya-L1 Space Weather Intelligence Platform. Before any nowcasting, forecasting, or machine learning can occur, raw telemetry from Aditya-L1’s diverse payload suite (SUIT, VELC, SoLEXS, HEL1OS, ASPEX, PAPA, MAG) must be validated, calibrated, synchronized, and assessed for quality.

This engine ensures that all downstream forecasting models operate exclusively on trustworthy, scientifically validated data, thereby preventing "garbage in, garbage out" (GIGO) scenarios.

## Architectural Philosophy
**"The Forecasting Engine should never begin with predictions. It must begin with trustworthy observations."**

Instead of mocking forecasts directly, this architecture simulates how real scientific telemetry pipelines operate:
1. **Raw Acquisition**: Simulated continuous data streams arriving at 1Hz from ISRO ground stations (simulated via WebSockets).
2. **Validation**: Packets are checked for integrity, timestamp continuity, and missing sequences.
3. **Calibration**: Raw digital numbers are converted to physical units using simulated calibration profiles (Gain/Offset).
4. **Synchronization**: Multi-instrument data (e.g., SUIT UV imaging + MAG magnetic field data) is time-aligned to a unified temporal grid.
5. **Quality Assessment**: Background estimation, noise analysis, and overall scientific confidence scoring are applied.
6. **Observation Provenance**: A complete lineage record is attached, ensuring traceability and reproducibility.

## Module Structure

The backend engine (`backend/observation_engine/`) comprises several decoupled, specialized modules:

### 1. `models.py`
Defines the strictly typed Pydantic models for the entire telemetry lifecycle, ensuring robust schema validation between backend stages and the frontend (via matching TypeScript definitions in `ForecastTypes.ts`).
- **EnrichedObservation**: The final, synthesized observation object.
- **ObservationProvenance**: Tracks versions, latency breakdowns, and IDs.
- **ValidationResult, CalibrationResult, SynchronizationResult, NoiseBackgroundResult, QualityResult**: Granular metadata for each pipeline stage.
- **PipelineStatus**: Real-time health metrics of the telemetry pipeline.

### 2. `validation.py`
Simulates telemetry packet validation. Checks for dropped packets, timestamps out of order, or payload corruption. A packet validation score determines whether the observation proceeds or requires interpolation.

### 3. `calibration.py`
Simulates the application of Level-0 to Level-1 calibration matrices. Simulates variations in calibration confidence due to instrument degradation or temperature fluctuations.

### 4. `synchronization.py`
Simulates the complex task of time-aligning disparate datasets. Instruments with different cadences (e.g., 10s vs 60s) are synchronized into a unified observation frame with computed time offsets and sync confidence.

### 5. `quality.py`
Evaluates the final data product. Detects noise percentages, evaluates signal stability, estimates soft/hard X-ray backgrounds, and flags anomalies (e.g., SATURATED, CALIBRATION_WARNING, TIMING_WARNING).

### 6. `metadata.py`
Manages instrument operational states and provenance tracking, computing detailed latency breakdowns across the acquisition, validation, calibration, and processing stages.

### 7. `manager.py` (ObservationManager)
The central orchestrator. It receives raw telemetry, routes it sequentially through the validation, calibration, synchronization, and quality pipelines, and emits the final `EnrichedObservation` ready for downstream systems.

## Data Flow & Integration

### Backend to Frontend Streaming
The unified `EnrichedObservation` stream is pushed to the frontend via WebSockets (`/ws/observation`), ensuring sub-second latency for live forecasting dashboards.

1. `api/main.py` mounts the `observation_engine` endpoints.
2. `api/ws/observation.py` generates the mock telemetry and pipes it through `ObservationManager`.
3. The WebSocket server pushes the validated `EnrichedObservation` to connected clients at 1Hz.

### Frontend Consumption
The frontend consumes this stream via a custom Zustand store (`forecastStore.ts`) and the `useObservationStream.ts` hook. The data strictly populates specialized scientific widgets:

- **ScientificObservationWorkspace**: Renders live telemetry values.
- **ObservationIntelligenceWorkspace**: Visualizes quality flags, confidence scores, and noise metrics.
- **OperatorWorkspace**: Monitors pipeline health, data freshness, latency, and instrument state.
- **ScientificWorkspace**: Visualizes the processing pipeline nodes (Validation -> Calibration -> Sync, etc.).

## Future Extensibility
By fully decoupling the **Observation Layer** from the **Forecasting Layer**, future updates can easily introduce:
1. Historical telemetry replay without altering forecast models.
2. Database persistence for observations (Observation Repository API).
3. Live ISRO data streams replacing the simulated data generator, with zero changes required to the frontend UI.
