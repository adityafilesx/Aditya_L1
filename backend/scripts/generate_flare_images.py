import os
import xspec
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from astropy.io import fits

# 1. Configuration
pi_file = "/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed/AL1_SOLEXS_SDD2_L1.pi"
rmf_file = "/Users/aditya1981/Downloads/solexs_tools-1.1/CALDB/response/rmf/solexs_gaussian_SDD2_v1.rmf"
arf_file = "/Users/aditya1981/Downloads/solexs_tools-1.1/CALDB/arf/solexs_arf_SDD2_v1.arf"

output_dir = "/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed/flare_evolution_frames"
os.makedirs(output_dir, exist_ok=True)

WINDOW_SIZE = 50  # Frames before and after peak (Total: 101 frames)

def find_peak_bin(file_path):
    print("Scanning .pi file to find the peak flare bin...")
    with fits.open(file_path) as hdul:
        data = hdul[1].data
        counts = data['COUNTS']
        total_counts = np.nansum(counts, axis=1)
        best_bin = np.nanargmax(total_counts) + 1  # 1-indexed for PyXspec
        return best_bin

def run():
    peak_bin = find_peak_bin(pi_file)
    start_bin = max(1, peak_bin - WINDOW_SIZE)
    end_bin = peak_bin + WINDOW_SIZE
    
    print(f"Flare Peak: Bin {peak_bin}. Extracting window: {start_bin} to {end_bin} ({(end_bin-start_bin)+1} frames).")
    
    # 2. XSPEC Global Setup
    xspec.Xset.chatter = 0
    xspec.Plot.device = "/null"
    xspec.Plot.xAxis = "keV"
    
    # We wrap in a loop over the window
    for i, current_bin in enumerate(range(start_bin, end_bin + 1)):
        print(f"Processing frame {i+1}/{(end_bin-start_bin)+1} (Bin {current_bin})...")
        xspec.AllData.clear()
        xspec.AllModels.clear()
        
        try:
            # Load spectrum
            s = xspec.Spectrum(f"{pi_file}{{{current_bin}}}")
            s.response = rmf_file
            s.response.arf = arf_file
            
            # Set manual constraints
            xspec.AllModels.systematic = 0.04
            s.ignore("**-2.8, 12.0-**")
            
            # Load the local model package
            xspec.AllModels.lmod("chspec", "/Users/aditya1981/.gemini/antigravity-ide/brain/ead5211d-dfba-45f4-a3a2-adaf18c4ec59/chspec_build")

            # Model setup (chisoth)
            m = xspec.Model("chisoth")
            m.chisoth.logT = 7.0  # start guess (10 MK)
            m.chisoth.Ar.frozen = False
            m.chisoth.Ca.frozen = False
            m.chisoth.Fe.frozen = False
            m.chisoth.Ni.frozen = False
            
            xspec.Fit.perform()
            
            # Extract fit stats
            best_logT = m.chisoth.logT.values[0]
            best_MK = (10 ** best_logT) / 1e6  # Convert logT in K to MK
            best_kT = (10 ** best_logT) / (1.16045e7)  # Convert logT to keV
            chi2 = xspec.Fit.statistic
            dof = xspec.Fit.dof
            red_chi2 = chi2 / dof if dof > 0 else 0
            
            best_Ar = m.chisoth.Ar.values[0]
            best_Ca = m.chisoth.Ca.values[0]
            best_Fe = m.chisoth.Fe.values[0]
            
            # Extract Plotting Data
            xspec.Plot("data")
            x = np.array(xspec.Plot.x())
            x_err = np.array(xspec.Plot.xErr())
            y = np.array(xspec.Plot.y())
            y_err = np.array(xspec.Plot.yErr())
            model_total = np.array(xspec.Plot.model())
            
            xspec.Plot("delchi")
            res = np.array(xspec.Plot.y())
            res_err = np.array(xspec.Plot.yErr())
            
            # Extract Components
            # Continuum (set abundances to 1.0 in log to turn off lines)
            m.chisoth.Ar.values = [1.0, -0.001, 0.0, 0.0, 10.0, 10.0]
            m.chisoth.Ca.values = [1.0, -0.001, 0.0, 0.0, 9.0, 9.0]
            m.chisoth.Fe.values = [1.0, -0.01, 0.0, 0.0, 8.5, 8.5]
            m.chisoth.Ni.values = [1.0, -0.01, 0.0, 0.0, 9.8, 9.8]
            xspec.Plot("data")
            continuum = np.array(xspec.Plot.model())
            
            # Ar Line
            m.chisoth.Ar.values = [best_Ar, -0.001, 0.0, 0.0, 10.0, 10.0]
            xspec.Plot("data")
            ar_line = np.array(xspec.Plot.model()) - continuum
            m.chisoth.Ar.values = [1.0, -0.001, 0.0, 0.0, 10.0, 10.0]
            
            # Ca Line
            m.chisoth.Ca.values = [best_Ca, -0.001, 0.0, 0.0, 9.0, 9.0]
            xspec.Plot("data")
            ca_line = np.array(xspec.Plot.model()) - continuum
            m.chisoth.Ca.values = [1.0, -0.001, 0.0, 0.0, 9.0, 9.0]
            
            # Fe Line
            m.chisoth.Fe.values = [best_Fe, -0.01, 0.0, 0.0, 8.5, 8.5]
            xspec.Plot("data")
            fe_line = np.array(xspec.Plot.model()) - continuum
            
            # Generate Figure
            fig = plt.figure(figsize=(12, 9))
            gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.05)
            
            ax1 = fig.add_subplot(gs[0])
            ax1.set_yscale('log')
            
            valid = y > 0
            if np.any(valid):
                ax1.errorbar(x[valid], y[valid], xerr=x_err[valid], yerr=y_err[valid], 
                             fmt='o', markersize=4, label='Observed Data', color='#4c72b0', elinewidth=1)
            
            ax1.plot(x, model_total, '-', label='Best Fit (bremss + lines)', color='#dd8452', linewidth=2.5)
            ax1.plot(x, continuum, '--', label='Thermal Bremsstrahlung', color='#55a868', linewidth=1.5)
            
            mask_ar = ar_line > 1e-4
            mask_ca = ca_line > 1e-4
            mask_fe = fe_line > 1e-4
            if np.any(mask_ar): ax1.plot(x[mask_ar], ar_line[mask_ar], ':', label='Ar XVII Line', color='#8172b2', linewidth=2)
            if np.any(mask_ca): ax1.plot(x[mask_ca], ca_line[mask_ca], ':', label='Ca XIX Line', color='#ccb974', linewidth=2)
            if np.any(mask_fe): ax1.plot(x[mask_fe], fe_line[mask_fe], ':', label='Fe XXV Line', color='#64b5cd', linewidth=2)
            
            ax1.set_ylabel('Counts / sec / keV', fontsize=14, fontweight='bold')
            ax1.set_title(f'SoLEXS Flare Evolution - Bin: {current_bin}', fontsize=16, fontweight='bold', pad=15)
            ax1.grid(True, linestyle=':', alpha=0.6)
            ax1.set_xlim(2.5, 12.5)
            ax1.set_ylim(bottom=1e-1, top=10**(np.ceil(np.log10(np.max(y)*5)))) if np.any(valid) else None
            ax1.legend(loc='lower left', fontsize=12, frameon=True, framealpha=0.9, shadow=True)
            
            stats_text = (f"Reduced $\\chi^2$ = {red_chi2:.2f} ({chi2:.1f}/{dof})\n"
                          f"Temperature = {best_MK:.1f} MK ({best_kT:.2f} keV)")
            props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='lightgray')
            ax1.text(0.95, 0.95, stats_text, transform=ax1.transAxes, fontsize=12,
                     verticalalignment='top', horizontalalignment='right', bbox=props)
            
            ax2 = fig.add_subplot(gs[1], sharex=ax1)
            ax2.errorbar(x, res, yerr=res_err, xerr=x_err, fmt='o', markersize=4, color='#4c72b0', elinewidth=1)
            ax2.axhline(0, color='black', linewidth=1)
            ax2.axhline(2, color='red', linestyle='--', alpha=0.5, linewidth=1)
            ax2.axhline(-2, color='red', linestyle='--', alpha=0.5, linewidth=1)
            
            ax2.set_xlabel('Energy (keV)', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Residuals ($\sigma$)', fontsize=14, fontweight='bold')
            ax2.grid(True, linestyle=':', alpha=0.6)
            ax2.set_ylim(-5, 5)
            
            plt.setp(ax1.get_xticklabels(), visible=False)
            
            out_png = os.path.join(output_dir, f"frame_{current_bin:05d}.png")
            plt.savefig(out_png, dpi=150, bbox_inches='tight')
            plt.close(fig)
        except Exception as e:
            print(f"Error on bin {current_bin}: {e}")
            continue

    print(f"\nCompilation complete! Images saved to {output_dir}")

if __name__ == "__main__":
    run()
