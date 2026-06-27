# Feature Quality Engine

The Feature Quality Engine assesses the statistical and scientific integrity of extracted feature vectors.

## Quality Scores
- **Completeness**: Ratio of non-missing features.
- **Reliability**: Weighted index of validation flags.
- **Consistency**: Score verifying cross-variable rules.
- **Freshness**: Measured processing latency relative to peak observations.

Vectors must pass an overall quality threshold to be marked as `ML_READY`.
