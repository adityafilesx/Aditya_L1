import os
import matplotlib.pyplot as plt
import numpy as np

def visualize_spectra(pi_file):
    # Initialize XSPEC
    import xspec
    
    # Load the CHIANTI thermal models (chspec)
    print("Loading CHIANTI thermal models (chspec)...")
    try:
        xspec.AllModels.lmod("chspec", "/Users/aditya1981/.gemini/antigravity-ide/brain/ead5211d-dfba-45f4-a3a2-adaf18c4ec59/chspec_build")
    except Exception as e:
        print(f"Warning: Could not load chspec local models: {e}")
        print("Continuing with standard models.")

    # Load spectrum
    print(f"Loading spectrum from {pi_file}...")
    try:
        # Load the first row of the Type II PHA file
        s = xspec.Spectrum(pi_file + "{1}")
        
        # Set response and ancillary files
        s.response = "/Users/aditya1981/Downloads/solexs_tools-1.1/CALDB/response/rmf/solexs_gaussian_SDD2_v1.rmf"
        s.response.arf = "/Users/aditya1981/Downloads/solexs_tools-1.1/CALDB/arf/solexs_arf_SDD2_v1.arf"
        
        # Add 4% systematic error
        xspec.AllModels.systematic = 0.04
        
        # Set a standard XSPEC model (chisoth, fallback to vvapec)
        try:
            m = xspec.Model("chisoth")
            m.chisoth.logT = 7.0
            m.chisoth.Ar.frozen = False
            m.chisoth.Ca.frozen = False
            m.chisoth.Fe.frozen = False
            m.chisoth.Ni.frozen = False
        except Exception:
            print("chisoth model not found, falling back to vvapec")
            m = xspec.Model("vvapec")
            m.vvapec.kT = 0.86
            m.vvapec.Ar.frozen = False
            m.vvapec.Ca.frozen = False
            m.vvapec.Fe.frozen = False
            m.vvapec.Ni.frozen = False
            
        # Ignore bad channels (uncertain below 2.8 keV, ignore above 12.0 keV)
        s.ignore("**-2.8, 12.0-**")
        
        # Perform the spectral fit
        print("Performing spectral fit with SoLEXS manual constraints...")
        xspec.Fit.perform()
        
        # We need Plot device to extract data
        xspec.Plot.device = "/null"
        xspec.Plot.xAxis = "keV"
        
        try:
            xspec.Plot("data")
        except Exception as e:
            print(f"Could not plot 'data': {e}")
            xspec.Plot.xAxis = "channel"
            xspec.Plot("counts")
        
        # Extract data for plotting
        x_vals = np.array(xspec.Plot.x())
        y_vals = np.array(xspec.Plot.y())
        x_err = np.array(xspec.Plot.xErr())
        y_err = np.array(xspec.Plot.yErr())
        try:
            model_vals = np.array(xspec.Plot.model())
        except Exception:
            model_vals = []
        
        plt.figure(figsize=(10, 6))
        plt.errorbar(x_vals, y_vals, xerr=x_err, yerr=y_err, fmt='o', markersize=3, label='Observed Spectrum')
        # Only plot model if it was successfully evaluated
        if len(model_vals) > 0 and len(model_vals) == len(x_vals):
            plt.plot(x_vals, model_vals, 'r-', linewidth=2, label='Thermal Model Fit')
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel('Energy (keV)')
        plt.ylabel('Counts / sec / keV')
        plt.title('Solar Flare Spectrum Visualization (Fitted)')
        plt.legend()
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        
        out_png = pi_file.replace('.pi', '_visualization.png')
        plt.savefig(out_png)
        print(f"Saved visualization to {out_png}")
        
    except Exception as e:
        print(f"Error visualizing spectrum: {e}")
        print("Note: If you receive a 'no response matrix' error, the .pi file lacks a RESPFILE header or the .rmf file is missing.")

if __name__ == "__main__":
    pi_file = "/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed/AL1_SOLEXS_SDD2_L1.pi"
    if os.path.exists(pi_file):
        visualize_spectra(pi_file)
    else:
        print(f"File not found: {pi_file}")
        print("Please extract the spectra first using extract_spectra.py")
