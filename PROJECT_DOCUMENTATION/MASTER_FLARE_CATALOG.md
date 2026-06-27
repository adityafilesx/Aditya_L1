# Master Flare Catalog

## Overview
The `MasterCatalog` serves as the definitive, immutable record of all scientifically validated solar flare events detected by the Nowcasting Engine. It acts as the single source of truth for downstream systems, including the Forecasting Engine and the Mission UI.

## Immutable and Versioned Architecture
Scientific integrity dictates that once an event is recorded, it should not be silently overwritten. The Master Catalog implements strict versioning:
- **Event ID**: A unique identifier generated upon the creation of a `UnifiedFlareEvent`.
- **Versioning**: As an active flare evolves (e.g., transitions from `ACTIVE` to `PEAK` to `DECAY`), new versions of the event are appended to the catalog rather than mutating the original record in place. 
- **Provenance Tracking**: Each entry includes references to the raw instrument events (SoLEXS and HEL1OS IDs) that contributed to its creation, allowing scientists to trace the exact lineage of the data.

## Schema
A typical catalog entry includes:
- `event_id`: Unique string (e.g., `FLR-20231024-001`).
- `version`: Integer starting at 1.
- `state`: Current state of the event (e.g., `ACTIVE`, `FINALIZED`).
- `start_time`: ISO-8601 timestamp.
- `peak_time`: Timestamp of peak flux (if applicable).
- `end_time`: Timestamp of event conclusion (if applicable).
- `xray_class`: Calculated GOES classification equivalent (e.g., M2.4) based on SoLEXS peak flux.
- `neupert_score`: The physics validation score from the Event Associator.
- `solexs_event_id`: Link to the raw SoLEXS detection.
- `helios_event_id`: Link to the raw HEL1OS detection.

## Output and Synchronization
The Master Catalog runs primarily in memory for rapid real-time access during the mission, but it is periodically synced to the persistent `NowcastRepository`. It emits events via the `NowcastState` payload sent over WebSocket to ensure the frontend `CatalogWidget` always displays the latest, scientifically validated flare list.
