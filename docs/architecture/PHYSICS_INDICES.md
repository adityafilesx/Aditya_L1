# Derived Physics Indices

To prepare the characterized flare catalog for downstream machine learning models (Milestone 4: Feature Store & Forecasting), the **Physics Engine** computes a series of scale-invariant, dimensionless indices. These indices capture the physical dynamics and ratios of each event.

## Calculated Indices

### 1. Heating Index ($H_I$)
measures the ratio of heating rate to cooling rate during the flare:
$$H_I = \frac{\text{Heating Rate}}{\text{Cooling Rate}}$$
- Values $> 1.0$ indicate impulsive, rapid energy injection followed by slow cooling.
- Values $< 1.0$ indicate slow, gradual heating with rapid cooling.

### 2. Cooling Index ($C_I$)
Measures the profile asymmetry between the decay phase and rise phase:
$$C_I = \frac{\text{Decay Time}}{\text{Rise Time}}$$
- Larger values indicate highly asymmetric flares (very common in solar flares where decay is much slower than rise).

### 3. Energy Release Index ($ER_I$)
A log-scale representation of the combined thermal and non-thermal energy:
$$ER_I = \log_{10}(E_{\text{thermal}} + E_{\text{non-thermal}})$$

### 4. Thermal Dominance ($TD$)
The fraction of the flare's total energy that is thermal in origin:
$$TD = \frac{E_{\text{thermal}}}{E_{\text{thermal}} + E_{\text{non-thermal}}}$$
- Ranges from $0.0$ (purely non-thermal burst) to $1.0$ (purely thermal heating).

### 5. Neupert Compliance ($NC$)
Indicates how closely the flare follows the Neupert effect model:
$$NC = \text{Neupert Score} \times \text{Neupert Consistency}$$
- Scores close to $1.0$ indicate the flare conforms perfectly to chromospheric evaporation model physics.

### 6. Spectral Hardness ($SH$)
Inverse of the spectral power-law index $\gamma$:
$$SH = \frac{1}{\gamma}$$
- Higher values represent a harder spectrum, corresponding to a greater proportion of high-energy non-thermal electrons.

### 7. Impulsiveness Index ($I_I$)
Measures how concentrated the energy release is relative to the mean flux:
$$I_I = \frac{F_{\text{peak}}}{\text{Integrated Flux} / \text{Duration}}$$
- Highly impulsive flares have large, sharp peaks relative to their average flux, leading to a higher $I_I$.
