# Event Timeline

## Overview
The `EventTimeline` module is a specialized, fast-access cache designed specifically to power the frontend `TimelineWidget`. While the Master Catalog maintains the entire history of all flares, the Event Timeline maintains a sliding temporal window of events (e.g., the last 60 minutes) to allow the frontend to render the visual timeline without polling the database.

## Architecture
The timeline holds:
- **Active Events**: Flares currently ongoing (state = `PRE_FLARE`, `ACTIVE`, `PEAK`, `DECAY`).
- **Recent Events**: Flares that have concluded (`FINALIZED`) but occurred within the specified rolling window (e.g., within the last 1-4 hours).
- **Synthetic Injection Markers**: Time periods where the Flare Simulator was active.

## Data Structure
The `TimelineWindow` is serialized and broadcast via WebSocket to the frontend inside the `NowcastState`. It is structured to minimize payload size while providing enough information for the D3/Plotly renderers to draw event brackets and markers over the telemetry flux lines.

```json
{
  "active_events": [
    {
      "id": "FLR-001",
      "state": "ACTIVE",
      "start": "2023-10-24T12:00:00Z"
    }
  ],
  "recent_events": [ ... ],
  "window_start": "2023-10-24T11:00:00Z"
}
```

## Lifecycle
1. The `NowcastManager` updates the `EventTimeline` every second.
2. New events from the `MasterCatalog` are added to the timeline.
3. As time progresses, events that fall outside the temporal window (`window_start`) are pruned from the timeline cache. They remain in the `MasterCatalog` and `NowcastRepository`, but are removed from the fast real-time broadcast payload.
