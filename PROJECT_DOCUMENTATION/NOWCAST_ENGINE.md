# Scientific Nowcasting Engine Architecture

## Overview
The Scientific Nowcasting Engine is the direct consumer of the Observation Engine. It implements the real-time detection of solar flares using independent sliding-window buffers and statistical thresholds (sigma and derivative tracking). It strictly prohibits predictions, focusing entirely on detecting what is happening right now with high confidence.

## Core Philosophy
The Forecasting Engine should never begin with predictions. It must begin with trustworthy observations. The Nowcasting Engine bridges the gap between raw telemetry and predictive modeling by establishing a real-time, statistically sound understanding of the current solar state.

## Components
- **Nowcast Manager (`nowcast_manager.py`)**: Coordinates the 1Hz telemetry feed into the two instrument detectors. Handles the state synchronization and lifecycle of the detection loop.
- **SoLEXS Detector (`solexs_detector.py`)**: Detects gradual thermal X-ray rises using adaptive EMA (Exponential Moving Average) and tracks long-duration flux increases.
- **HEL1OS Detector (`helios_detector.py`)**: Detects impulsive hard X-ray bursts using a strict sigma threshold against an adaptive background buffer.
- **Event Associator (`event_association.py`)**: Checks temporal overlap and Neupert effect timing to associate single-instrument detections into Unified Flares.
- **Master Flare Catalog (`master_catalog.py`)**: The immutable, versioned record of all events, tracking provenance and evolution.
- **Event Timeline (`event_timeline.py`)**: Real-time sliding window of active and recent events, designed for fast UI rendering.
- **Nowcast Repository (`nowcast_repository.py`)**: Persistence layer using SQLite for historical search, replay, and statistics interface.
- **Flare Simulator (`flare_simulator.py`)**: Generates synthetic deterministic flare profiles (Standard, Impulsive, Long Duration) for rigorous testing and UI validation.

## Data Flow Pipeline
1. **Telemetry Ingestion**: `EnrichedObservation` enters `NowcastManager`.
2. **Simulation Injection (Optional)**: `FlareSimulator` injects synthetic flares if active.
3. **Parallel Detection**: The observation is routed to both `SolexsDetector` and `HeliosDetector` simultaneously.
4. **State Evaluation**: Each detector returns its current state (NOMINAL, PRE_FLARE, ACTIVE, PEAK, DECAY) and optionally a `DetectorEvent`.
5. **Association**: If events are active, they are passed to the `EventAssociator`.
6. **Cataloging**: Unified events are stored in the `MasterCatalog`.
7. **Broadcast**: The unified `NowcastState` is broadcast via WebSocket to the frontend `useNowcastStream` hook.

## strict Tiered Approach
The platform strictly adheres to the following tiering:
**Raw Telemetry** → **Observation Engine** (Validation, Calibration, Sync) → **Nowcasting Engine** (Detection, Association, Cataloging) → **Forecasting Engine** (Machine Learning, Predictions).

The Nowcasting Engine represents the completion of ISRO Deliverables 1 (Data Validation/Calibration mapping to Observation Engine) and 2 (Real-time Flare Detection).
