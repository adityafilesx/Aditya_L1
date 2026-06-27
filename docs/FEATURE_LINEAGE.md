# Feature Lineage Engine

Complete end-to-end lineage tracking guarantees traceability from raw telemetry down to output feature vectors.

## Lineage Path
```
Observation (ID, Instrument)
      ↓
Nowcast (Master Catalog Event)
      ↓
Physics (Characterized Product)
      ↓
Validation (Gate Check)
      ↓
Normalization (Scaling/Transform Metadata)
      ↓
Feature Vector (ML Ready Store)
```
Each vector maintains a node trace list for auditing.
