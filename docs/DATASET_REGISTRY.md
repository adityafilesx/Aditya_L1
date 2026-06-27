# Dataset Registry

The Dataset Registry registers compiled snapshots of training data.

## Fields Logged

- **`dataset_id`**: Unique reference string.
- **`dataset_version`**: Semantic version.
- **`feature_version`**: Feature catalog version.
- **`label_version`**: Target label version.
- **`training_split`**: Fraction of data in training partition.
- **`validation_split`**: Fraction of data in validation partition.
- **`testing_split`**: Fraction of data in testing partition.
- **`creation_time`**: Timestamp.
- **`checksum`**: MD5 value verifying data integrity.
- **`source`**: Underlying Feature Store identifier.
- **`time_window`**: Historical buffer size (e.g. `24h`).
- **`forecast_horizon`**: Target predictive window (e.g. `1h`).
