# Feature Statistics Engine

The Feature Statistics Engine computes running statistical distributions and pipeline metrics for active monitoring.

## Tracked Metrics
- **Mean, Median, Standard Deviation**: Running averages of active features.
- **Outlier Percentage**: Outliers calculated using the `1.5 * IQR` rule.
- **Missing Percentage**: Rates of unpopulated variables.
- **Pipeline Failure Rates**: Success rates of validations and normalizations.
