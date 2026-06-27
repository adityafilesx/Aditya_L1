# Feature Normalization Engine

The Feature Normalization Engine standardizes and scales raw values to prevent numerical instability and model bias.

## Normalization Methods
- **MinMax Scaling**: Scales values strictly to `[0.0, 1.0]` based on allowed registry bounds. Used for temporal rates and fluxes.
- **Standard Scaling**: Standardizes features to zero mean and unit variance based on reference mission datasets. Used for temperature and heating rates.
- **None**: Retains raw values where indices are already dimensionless ratios.

Dual-representation storage (raw alongside normalized values) is preserved.
