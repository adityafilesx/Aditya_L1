import os
import sys
import numpy as np
import pandas as pd
from astropy.io import fits

def extract_time_resolved_params(pi_file, rmf_file, arf_file, out_csv):
    import xspec
    
    # Load the local model package
    print("Loading CHIANTI thermal models (chspec)...")
    try:
        xspec.AllModels.lmod("chspec", "/Users/aditya1981/.gemini/antigravity-ide/brain/ead5211d-dfba-45f4-a3a2-adaf18c4ec59/chspec_build")
    except Exception as e:
        print(f"Warning: Could not load chspec local models: {e}")
        print("Continuing with standard models.")

    # 1. Determine number of spectra
    print(f"Opening {pi_file} to determine number of time bins...")
    with fits.open(pi_file) as hdul:
        # Usually the spectrum is in the first extension (SPECTRUM)
        spec_ext = hdul['SPECTRUM']
        num_spectra = len(spec_ext.data)
        
    print(f"Found {num_spectra} spectra in the Type II PHA file.")
    
    # Configure XSPEC
    xspec.Fit.statMethod = "chi"
    xspec.Xset.chatter = 0  # Reduce verbosity
    
    results = []
    
    # Process up to a certain number of spectra for efficiency in this test, or all if small
    print(f"Processing all {num_spectra} time bins...")
    
    for i in range(1, num_spectra + 1):
        try:
            # Clear previous data and models
            xspec.AllData.clear()
            xspec.AllModels.clear()
            
            # Load spectrum
            s = xspec.Spectrum(f"{pi_file}{{{i}}}")
            s.response = rmf_file
            s.response.arf = arf_file
            
            # Add 4% systematic error as per SoLEXS manual
            xspec.AllModels.systematic = 0.04
            
            # Ignore bad channels (Below 2.8 keV is uncertain, ignore above 12.0 keV)
            s.ignore("**-2.8, 12.0-**")
            
            # Set model: chisoth + powerlaw (fallback to vvapec + powerlaw)
            try:
                m = xspec.Model("chisoth + powerlaw")
                m.chisoth.logT = 7.0
                m.chisoth.Ar.frozen = False
                m.chisoth.Ca.frozen = False
                m.chisoth.Fe.frozen = False
                m.chisoth.Ni.frozen = False
                m.powerlaw.PhoIndex = 3.0
                
                # Perform fit
                xspec.Fit.perform()
                
                # Extract parameters
                T_val = m.chisoth.logT.values[0] # This is log(T) in Kelvin
                EM_norm = m.chisoth.norm.values[0]
                gamma = m.powerlaw.PhoIndex.values[0]
                
            except Exception:
                m = xspec.Model("vvapec + powerlaw")
                m.vvapec.kT = 0.86  # ~10 MK
                m.vvapec.Ar.frozen = False
                m.vvapec.Ca.frozen = False
                m.vvapec.Fe.frozen = False
                m.vvapec.Ni.frozen = False
                m.powerlaw.PhoIndex = 3.0
                
                # Perform fit
                xspec.Fit.perform()
                
                # Extract parameters
                T_val = m.vvapec.kT.values[0] # This is kT in keV
                EM_norm = m.vvapec.norm.values[0]
                gamma = m.powerlaw.PhoIndex.values[0]
            
            # Calculate Hardness Ratio
            # Soft band (2.8 - 5.0 keV)
            s.notice("all")
            s.ignore("**-2.8, 5.0-**")
            soft_rate = s.rate[0]  # total count rate in noticed channels
            
            # Hard band (5.0 - 12.0 keV)
            s.notice("all")
            s.ignore("**-5.0, 12.0-**")
            hard_rate = s.rate[0]
            
            hr = hard_rate / soft_rate if soft_rate > 0 else 0.0
            
            results.append({
                'Time_Bin': i,
                'Temperature_val': T_val,
                'Emission_Measure_norm': EM_norm,
                'Spectral_Index_Gamma': gamma,
                'Hardness_Ratio': hr,
                'Soft_Rate': soft_rate,
                'Hard_Rate': hard_rate
            })
            
        except Exception as e:
            print(f"Failed at bin {i}: {e}")
            results.append({
                'Time_Bin': i,
                'Temperature_val': np.nan,
                'Emission_Measure_norm': np.nan,
                'Spectral_Index_Gamma': np.nan,
                'Hardness_Ratio': np.nan,
                'Soft_Rate': np.nan,
                'Hard_Rate': np.nan
            })
            
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Compute derivatives (assuming dt = 1 second per bin)
    dt = 1.0
    df['dT_dt'] = df['Temperature_val'].diff() / dt
    df['dEM_dt'] = df['Emission_Measure_norm'].diff() / dt
    df['dGamma_dt'] = df['Spectral_Index_Gamma'].diff() / dt
    df['dHR_dt'] = df['Hardness_Ratio'].diff() / dt
    
    # Save to CSV
    df.to_csv(out_csv, index=False)
    print(f"Extraction complete. Results saved to {out_csv}")
    
if __name__ == "__main__":
    pi_file = "/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed/AL1_SOLEXS_SDD2_L1.pi"
    rmf_file = "/Users/aditya1981/Downloads/solexs_tools-1.1/CALDB/response/rmf/solexs_gaussian_SDD2_v1.rmf"
    arf_file = "/Users/aditya1981/Downloads/solexs_tools-1.1/CALDB/arf/solexs_arf_SDD2_v1.arf"
    out_csv = "/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed/AL1_SOLEXS_SDD2_L1_time_resolved_params.csv"
    
    if os.path.exists(pi_file):
        extract_time_resolved_params(pi_file, rmf_file, arf_file, out_csv)
    else:
        print("PI file not found.")
