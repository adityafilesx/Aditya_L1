import os
import sys
import numpy as np
import pandas as pd
from astropy.io import fits

def extract_flare_params(pi_file, rmf_file, arf_file, out_csv, start_bin, end_bin):
    import xspec
    
    print("Loading CHIANTI thermal models (chspec)...")
    try:
        xspec.AllModels.lmod("chspec", "/Users/aditya1981/.gemini/antigravity-ide/brain/ead5211d-dfba-45f4-a3a2-adaf18c4ec59/chspec_build")
    except Exception as e:
        print(f"Warning: Could not load chspec local models: {e}")
    
    xspec.Fit.statMethod = "chi"
    xspec.Xset.chatter = 0
    
    results = []
    print(f"Processing time bins from {start_bin} to {end_bin}...")
    
    for i in range(start_bin, end_bin + 1):
        try:
            xspec.AllData.clear()
            xspec.AllModels.clear()
            
            s = xspec.Spectrum(f"{pi_file}{{{i}}}")
            s.response = rmf_file
            s.response.arf = arf_file
            xspec.AllModels.systematic = 0.04
            
            s.ignore("**-2.8, 12.0-**")
            
            try:
                m = xspec.Model("chisoth + powerlaw")
                m.chisoth.logT = 7.0
                m.chisoth.Ar.frozen = False
                m.chisoth.Ca.frozen = False
                m.chisoth.Fe.frozen = False
                m.chisoth.Ni.frozen = False
                m.powerlaw.PhoIndex = 3.0
                
                xspec.Fit.perform()
                T_val = m.chisoth.logT.values[0]
                EM_norm = m.chisoth.norm.values[0]
                gamma = m.powerlaw.PhoIndex.values[0]
                
            except Exception:
                m = xspec.Model("vvapec + powerlaw")
                m.vvapec.kT = 0.86
                m.vvapec.Ar.frozen = False
                m.vvapec.Ca.frozen = False
                m.vvapec.Fe.frozen = False
                m.vvapec.Ni.frozen = False
                m.powerlaw.PhoIndex = 3.0
                
                xspec.Fit.perform()
                T_val = m.vvapec.kT.values[0]
                EM_norm = m.vvapec.norm.values[0]
                gamma = m.powerlaw.PhoIndex.values[0]
            
            s.notice("all")
            s.ignore("**-2.8, 5.0-**")
            soft_rate = s.rate[0]
            
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
            
            if i % 100 == 0:
                print(f"Processed up to bin {i}...")
                
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
            
    df = pd.DataFrame(results)
    dt = 1.0
    df['dT_dt'] = df['Temperature_val'].diff() / dt
    df['dEM_dt'] = df['Emission_Measure_norm'].diff() / dt
    df['dGamma_dt'] = df['Spectral_Index_Gamma'].diff() / dt
    df['dHR_dt'] = df['Hardness_Ratio'].diff() / dt
    
    df.to_csv(out_csv, index=False)
    print(f"Extraction complete. Results saved to {out_csv}")

if __name__ == "__main__":
    pi_file = "/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed/20240212/AL1_SOLEXS_SDD2_L1.pi"
    rmf_file = "/Users/aditya1981/Downloads/solexs_tools-1.1/CALDB/response/rmf/solexs_gaussian_SDD2_v1.rmf"
    arf_file = "/Users/aditya1981/Downloads/solexs_tools-1.1/CALDB/arf/solexs_arf_SDD2_v1.arf"
    out_csv = "/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed/20240212/flare_params.csv"
    
    start_time_s = 3 * 3600 + 23 * 60
    end_time_s = 4 * 3600 + 10 * 60
    
    # +1 because XSPEC spectra are 1-indexed, assuming 00:00:00 is spectrum 1
    extract_flare_params(pi_file, rmf_file, arf_file, out_csv, start_time_s + 1, end_time_s + 1)
