import os
import xspec
import pandas as pd
import numpy as np
from astropy.io import fits

def create_xspec_environment():
    """Initializes and configures the XSPEC environment."""
    xspec.Xset.chatter = 10
    xspec.Xset.logChatter = 20
    log_file = xspec.Xset.openLog("aditya_joint_fit.log")
    
    # Configure fitting settings
    xspec.Fit.statMethod = "chi"
    xspec.Fit.method = "leven"
    xspec.Fit.nIterations = 200
    xspec.Fit.criticalDelta = 1e-3
    return log_file

def load_and_prepare_spectra(solexs_pi, helios_pi):
    """
    Loads spectral data into XSPEC data groups and assigns calibration files.
    Data Group 1: SoLEXS (Soft X-rays)
    Data Group 2: HEL1OS CZT1/2 (Hard X-rays)
    """
    xspec.AllData.clear()
    
    # 1. Load SoLEXS Spectrum (SDD2 Preferred to avoid saturation)
    s_spectrum = xspec.Spectrum(solexs_pi)
    
    # 2. Load HEL1OS Spectrum (CZT1 or CZT2)
    h_spectrum = xspec.Spectrum(helios_pi)
    
    # Generate Dummy Response Matrices to bypass missing ISRO proprietary .rmf/.arf files
    xspec.AllData.dummyrsp(0.1, 150.0, 341)
    
    print(f"Successfully loaded spectra into XSPEC.")
    return s_spectrum, h_spectrum

def apply_instrument_filters():
    """
    Applies energy range constraints based on instrument manuals to eliminate 
    uncalibrated thresholds and noise.
    """
    # SoLEXS: Recommended range for fitting is above 2.8 keV due to low-energy uncertainty.
    # Upper bound restricted to 12.0 keV based on typical signal-to-noise.
    xspec.AllData(1).ignore("**-2.8 12.0-**")
    
    # HEL1OS CZT: Recommended lowest energy range is >30 keV (typically 33-35 keV).
    # Upper limit restricted to ~106 keV where count flux dominates background.
    xspec.AllData(2).ignore("**-33.0 106.0-**")
    
    # Apply systematic errors (SoLEXS: 4%, HEL1OS: default calibration stability)
    xspec.AllData(1).systematic = 0.04
    xspec.AllData(2).systematic = 0.02

def define_spectral_model():
    """
    Defines a composite multi-thermal and non-thermal astrophysical model:
    Model: phabs * (bremss + powerlaw)
    - phabs: Photoelectric Absorption
    - bremss: Thermal Bremsstrahlung (Soft X-ray continuum)
    - powerlaw: Non-thermal powerlaw (Hard X-ray tail)
    """
    # Define model wrapper
    model_expression = "phabs * (bremss + powerlaw)"
    m = xspec.Model(model_expression)
    
    # Set Initial Empirical Parameter Guesses & Constraints
    m.phabs.nH = 0.1
    
    m.bremss.kT = 1.5        # ~17 MK peak flare plasma temperature in keV
    m.powerlaw.PhoIndex = 4.1 # Electron spectral index
    
    return m

def execute_fit_and_save_metadata(output_prefix):
    """Executes the optimization loop and logs labeled parameters for future iteration."""
    print("Beginning optimization loop...")
    xspec.Fit.perform()
    
    # Evaluate goodness of fit
    reduced_chi = xspec.Fit.chi / xspec.Fit.dof
    print(f"Optimization complete. Reduced Chi-Squared: {reduced_chi:.4f}")
    
    # Save the fit results file (.xcm) for serialization/future iterations
    xspec.Xset.save(f"{output_prefix}_best_fit.xcm", info="model")
    
    # Extract structural performance metadata
    fit_metadata = {
        "reduced_chi_sq": reduced_chi,
        "dof": xspec.Fit.dof,
        "statistic": xspec.Fit.statistic
    }
    return fit_metadata

if __name__ == "__main__":
    # Standard Pipeline Execution Workflow
    log = create_xspec_environment()
    
    # Replace filenames with paths generated from your parquet pipeline conversion scripts
    solexs_file = "data/processed/AL1_SOLEXS_SDD2_L1.pi{1}"
    helios_file = "data/processed/hellos_czt1_spectra.fits{1}"
    
    s_spec, h_spec = load_and_prepare_spectra(solexs_file, helios_file)
    
    # apply_instrument_filters()
    define_spectral_model()
    execute_fit_and_save_metadata(output_prefix="aditya_L1_flare_peak")
    
    xspec.Xset.closeLog()
