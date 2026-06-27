# Flare Classification Engine

The **Flare Classification Engine** translates the arbitrary units of the simulator's peak soft X-ray flux into standard scientific classifications used by organizations like ISRO and NOAA (the GOES classification scale: A, B, C, M, X).

## GOES Mapping Rules
The engine maps peak flux values using a log-linear scale to simulate actual solar irradiance levels in Watts per square meter ($W/m^2$):
- **A-Class**: Irradiance $< 10^{-7} W/m^2$
- **B-Class**: $10^{-7} \le \text{Irradiance} < 10^{-6} W/m^2$
- **C-Class**: $10^{-6} \le \text{Irradiance} < 10^{-5} W/m^2$
- **M-Class**: $10^{-5} \le \text{Irradiance} < 10^{-4} W/m^2$
- **X-Class**: Irradiance $\ge 10^{-4} W/m^2$

The specific empirical mapping formula used by the engine is:
$$\text{Irradiance} = 10^{2.0 \times \log_{10}(F_{peak}) - 10.0}$$
For example:
- A peak flux of $100$ maps to $10^{-6} W/m^2$ (**C1.0**)
- A peak flux of $316$ maps to $10^{-5} W/m^2$ (**M1.0**)
- A peak flux of $1000$ maps to $10^{-4} W/m^2$ (**X1.0**)

## Output Structure
- **`goes_class`**: Enum value (`A`, `B`, `C`, `M`, `X`, `UNKNOWN`).
- **`goes_subclass`**: Standard notation string, e.g. `"M2.3"` or `"X1.5"`.
- **`classification_confidence`**: Confidence bound scaled by data quality and signal-to-noise ratio.
