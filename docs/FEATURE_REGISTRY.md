# Feature Registry

The Central Feature Registry is the authoritative source of truth for every feature engineering variable generated in the platform. No feature may exist outside this registry.

## Registry Schema
Each feature registered stores:
- **Feature ID**: Unique identifier (e.g. `F-THERM-001`).
- **Feature Name**: Code variable representation.
- **Description**: Explanation of the variable.
- **Scientific Meaning**: Physical interpretation in solar flare physics.
- **Units**: S.I. or standardized units (e.g. MK, W/m^2, seconds).
- **Category**: Class grouping (temporal, flux, thermal, nonthermal, indices).
- **Source Engine**: Backend logic producing it (characterization, indices, thermal).
- **Dependencies**: Prerequisites features.
- **Allowed Range**: Scientific bounding limits.
- **Normalization Strategy**: Strategy applied at runtime (minmax, standard, none).

## Active Governed Variables
1. `rise_time` (F-TEMP-001): Rise duration, minmax scaled.
2. `decay_time` (F-TEMP-002): Decay duration, minmax scaled.
3. `duration` (F-TEMP-003): Total flare duration, minmax scaled.
4. `peak_flux` (F-FLUX-001): Peak flux level, minmax scaled.
5. `peak_temperature` (F-THERM-001): Plasma temp, standard scaled.
6. `heating_index` (F-IND-001): Heat index ratio, standard scaled.
7. `thermal_dominance` (F-IND-002): Thermal energy ratio, unscaled.
