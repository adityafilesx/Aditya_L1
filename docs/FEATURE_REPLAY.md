# Feature Replay Engine

The Feature Replay Engine allows reproducing historical feature vectors and exporting compiled datasets.

## Functionality
- **Time Windows**: Replays vectors for the last hour, last day, or custom ranges.
- **Label Alignment**: Employs the Dataset Builder to look ahead at subsequent event chronological order and generate actual targets.
- **Exporting Options**: Generates CSV, Parquet, JSON, and NumPy files.
