# Nowcast API Reference

## REST API (Base: `/api/nowcasting`)

- `GET /state`
  - Returns the complete real-time `NowcastState` snapshot, including detector states, the active event, and recent catalog items.

- `GET /catalog`
  - Returns the most recent 50 entries in the Master Flare Catalog.

- `GET /catalog/active`
  - Returns all currently active flare catalog entries.

- `GET /catalog/{master_id}`
  - Returns a specific catalog entry by its `master_id`.

- `GET /detector/solexs`
  - Returns the current internal state of the SoLEXS detector (flux, background, state, confidence).

- `GET /detector/helios`
  - Returns the current internal state of the HEL1OS detector.

- `GET /timeline`
  - Returns the active and recent event timeline.

- `GET /timeline/replay?start={start}&end={end}`
  - Replays historical events within the ISO8601 time window.

- `GET /repository/statistics`
  - Returns aggregate statistical metrics from the repository.

- `GET /repository/export`
  - Exports all events from the repository as a raw JSON dump.

## WebSocket API

- `ws://<host>/ws/nowcasting/stream`
  - Broadcasts the complete `NowcastState` payload at 1Hz, driving the live UI widgets, timelines, and catalogs.
