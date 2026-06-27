# Training Pipeline

The training pipeline orchestrates the transition from raw feature vectors to calibrated, registered models.

## Pipeline Flow

1. **Load Dataset**: Compiles feature matrices and label definitions from the `ScientificFeatureStore` via the `DatasetBuilder`.
2. **Validate Dataset**: Assesses feature completeness, missing value ratios, and class imbalances.
3. **Split Dataset**: Splits datasets chronologically using time-series cross-validation. Random splits are strictly forbidden to avoid future leaks.
4. **Train Models**: Executes training across all selected algorithms (XGBoost, LightGBM, Random Forest, CatBoost, LSTM, GRU, Temporal CNN, Transformer).
5. **Evaluate & Calibrate**: Computes metrics and calibrates probabilities to satisfy ISRO requirements.
6. **Register Models**: Logs metadata and persists serialized states.

## Cross Validation Strategies

- **Walk Forward**: Expands the training window iteratively, validating on the next block.
- **Rolling Window**: Fixed-size sliding training window.
- **Blocked Time Series**: Splitting data into non-overlapping chronological blocks of train/test subsets.
