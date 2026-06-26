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
output_file = "/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed/AL1_SOLEXS_SDD2_L1_advanced_fit.png"

def find_peak_bin(file_path):
    print("Scanning .pi file to find the peak flare bin...")
    try:
        with fits.open(file_path) as hdul:
            data = hdul[1].data
            counts = data['COUNTS']
            total_counts = np.nansum(counts, axis=1)
            best_bin = np.nanargmax(total_counts) + 1  # 1-indexed for PyXspec
            max_c = np.nanmax(total_counts)
            print(f"Found peak at bin {best_bin} with {max_c} total counts.")
            return best_bin
    except Exception as e:
        print(f"Could not read FITS file with astropy: {e}. Defaulting to bin 1000.")
        return 1000

def run():
    peak_bin = find_peak_bin(pi_file)
    
    # 2. XSPEC Setup
    xspec.Xset.chatter = 0
    xspec.AllData.clear()
    xspec.AllModels.clear()
    
    # Load spectrum
    s = xspec.Spectrum(f"{pi_file}{{{peak_bin}}}")
    s.response = rmf_file
    s.response.arf = arf_file
    
    # Set manual constraints
    xspec.AllModels.systematic = 0.04
    s.ignore("**-2.8, 12.0-**")
    
    # Load the local model package
    xspec.AllModels.lmod("chspec", "/Users/aditya1981/.gemini/antigravity-ide/brain/ead5211d-dfba-45f4-a3a2-adaf18c4ec59/chspec_build")

    # 3. Model setup (chisoth)
    print("Fitting chisoth model...")
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
    
    # Extract best fit abundances
    best_Ar = m.chisoth.Ar.values[0]
    best_Ca = m.chisoth.Ca.values[0]
    best_Fe = m.chisoth.Fe.values[0]
    best_Ni = m.chisoth.Ni.values[0]
    
    # 4. Extract Plotting Data
    xspec.Plot.device = "/null"
    xspec.Plot.xAxis = "keV"
    xspec.Plot("data")
    
    x = np.array(xspec.Plot.x())
    x_err = np.array(xspec.Plot.xErr())
    y = np.array(xspec.Plot.y())
    y_err = np.array(xspec.Plot.yErr())
    model_total = np.array(xspec.Plot.model())
    
    xspec.Plot("delchi")
    res = np.array(xspec.Plot.y())
    res_err = np.array(xspec.Plot.yErr())
    
    # 5. Extract Components
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
    
    # 6. Matplotlib Visualization
    print("Generating Matplotlib visualization...")
    plt.style.use('default')
    fig = plt.figure(figsize=(12, 9))
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.05)
    
    # Top Panel: Spectrum
    ax1 = fig.add_subplot(gs[0])
    ax1.set_yscale('log')
    
    # Only plot points where y > 0 to avoid log(0) issues
    valid = y > 0
    ax1.errorbar(x[valid], y[valid], xerr=x_err[valid], yerr=y_err[valid], 
                 fmt='o', markersize=4, label='Observed Data', color='#4c72b0', elinewidth=1)
    
    ax1.plot(x, model_total, '-', label='Best Fit (bremss + lines)', color='#dd8452', linewidth=2.5)
    ax1.plot(x, continuum, '--', label='Thermal Bremsstrahlung', color='#55a868', linewidth=1.5)
    
    # Mask zeros for lines so log scale doesn't break or draw lines to bottom
    mask_ar = ar_line > 1e-4
    mask_ca = ca_line > 1e-4
    mask_fe = fe_line > 1e-4
    if np.any(mask_ar): ax1.plot(x[mask_ar], ar_line[mask_ar], ':', label='Ar XVII Line', color='#8172b2', linewidth=2)
    if np.any(mask_ca): ax1.plot(x[mask_ca], ca_line[mask_ca], ':', label='Ca XIX Line', color='#ccb974', linewidth=2)
    if np.any(mask_fe): ax1.plot(x[mask_fe], fe_line[mask_fe], ':', label='Fe XXV Line', color='#64b5cd', linewidth=2)
    
    ax1.set_ylabel('Counts / sec / keV', fontsize=14, fontweight='bold')
    ax1.set_title(f'SoLEXS Flare Spectral Fit (Peak Bin: {peak_bin})', fontsize=16, fontweight='bold', pad=15)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.set_xlim(2.5, 12.5)
    ax1.set_ylim(bottom=1e-1, top=10**(np.ceil(np.log10(np.max(y)*5))))
    ax1.legend(loc='lower left', fontsize=12, frameon=True, framealpha=0.9, shadow=True)
    
    # Text box for stats
    stats_text = (f"Reduced $\\chi^2$ = {red_chi2:.2f} ({chi2:.1f}/{dof})\n"
                  f"Temperature = {best_MK:.1f} MK ({best_kT:.2f} keV)")
    props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='lightgray')
    ax1.text(0.95, 0.95, stats_text, transform=ax1.transAxes, fontsize=12,
             verticalalignment='top', horizontalalignment='right', bbox=props)
    
    # Bottom Panel: Residuals
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.errorbar(x, res, yerr=res_err, xerr=x_err, fmt='o', markersize=4, color='#4c72b0', elinewidth=1)
    ax2.axhline(0, color='black', linewidth=1)
    ax2.axhline(2, color='red', linestyle='--', alpha=0.5, linewidth=1)
    ax2.axhline(-2, color='red', linestyle='--', alpha=0.5, linewidth=1)
    
    ax2.set_xlabel('Energy (keV)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Residuals ($\sigma$)', fontsize=14, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.set_ylim(-5, 5)
    
    # Remove x-ticks from top panel
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    # Save output
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved highly detailed visualization to {output_file}")

if __name__ == "__main__":
    run()
