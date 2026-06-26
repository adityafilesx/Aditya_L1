# Aditya-L1 Physics-Informed Intelligence Handbook

## 1. Wavelet Intelligence
We utilize the Continuous Wavelet Transform (CWT) using the Complex Morlet wavelet (`cmor1.5-1.0`) to extract the dominant oscillation scale. Discrete Wavelet Transforms (DWT) using `db2` extract the high-frequency burst intensity (D1 coefficients) to detect microflares superimposed on the main flare profile.

## 2. Thermodynamic Intelligence
Without full spectral inversion (XSPEC), we use an empirical fallback based on the hardness ratio $HR = F_{hard} / F_{soft}$.
* $T (MK) \approx 15 \sqrt{HR}$
* $EM \approx F_{soft} / \sqrt{T}$

## 3. Neupert Effect
The Neupert score measures the Pearson correlation between the hard X-ray flux and the time derivative of the soft X-ray flux:
$$ r = \text{corr}(F_{hard}, \frac{dF_{soft}}{dt}) $$
A high score ($>0.7$) confirms impulsive electron beam heating.

## 4. Signal Processing & Entropy
* **Shannon Entropy**: Measures the information content/disorder in the amplitude histogram.
* **Spectral Entropy**: Evaluates the flatness of the Power Spectral Density (PSD).
* **Spectral Flatness**: $\exp(\overline{\ln(PSD)}) / \overline{PSD}$. Detects whether the signal is noise-like (high flatness) or tonal/oscillatory (low flatness).

## 5. Morphology & Segmentation
The timeline automatically slices into:
1. **Preheating**: $F < 0.1 F_{peak}$ and $dF/dt > 0$
2. **Impulsive Rise**: $dF/dt \gg 0$
3. **Peak**: Global maximum of the segment.
4. **Decay**: Exponential drop-off phase.
