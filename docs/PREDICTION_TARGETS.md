# Prediction Targets

This registry defines forecasting targets that will consume the generated feature vectors.

## Classification Targets
- **goes_probability_30m**: Class A/B/C/M/X probability in the next 30 minutes.
- **goes_probability_1h**: Class A/B/C/M/X probability in the next 1 hour.
- **goes_probability_6h**: Class A/B/C/M/X probability in the next 6 hours.
- **goes_probability_24h**: Class A/B/C/M/X probability in the next 24 hours.

## Regression Targets
- **expected_peak_flux**: Expected soft X-ray peak flux magnitude of the next flare event.
- **expected_duration**: Expected duration of the next event.
