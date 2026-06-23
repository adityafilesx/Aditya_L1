import nbformat as nbf
from pathlib import Path

nb = nbf.v4.new_notebook()

cells = [
    """import sys
sys.path.insert(0, '..')  # add project root
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

from aditya_flare.data.readers.solexs_reader import read_solexs_lc, read_solexs_gti
from aditya_flare.data.readers.helios_reader import read_helios_lc_all, read_helios_gti
from aditya_flare.data.readers.time_utils import unix_to_utc, mjd_to_utc
from aditya_flare.data.merger.data_merger import merge_instruments, save_merged

# Set your data directories here
SOLEXS_DATA_DIR = Path("../data/raw/2024-07-17/solexs/")
HELIOS_DATA_DIR = Path("../data/raw/2024-07-17/helios/")
""",
    """# AL1_SOLEXS_20240717_SDD2_L1.lc.gz  (preferred — SDD1 saturates at M-class)
# AL1_SOLEXS_20240717_SDD2_L1.gti.gz

solexs_lc_file = SOLEXS_DATA_DIR / "AL1_SOLEXS_20240717_SDD2_L1.lc.gz"
solexs_gti_file = SOLEXS_DATA_DIR / "AL1_SOLEXS_20240717_SDD2_L1.gti.gz"

try:
    solexs_df = read_solexs_lc(solexs_lc_file)
    solexs_gti = read_solexs_gti(solexs_gti_file)
    print(f"SoLEXS: {len(solexs_df)} rows, detector={solexs_df['detector'].iloc[0]}")
    print(f"Time range: {solexs_df['time_utc'].min()} → {solexs_df['time_utc'].max()}")
    print(f"GTI intervals: {len(solexs_gti)}")
    print(f"Count rate range: {solexs_df['counts'].min():.1f} — {solexs_df['counts'].max():.1f} cts/s")
    display(solexs_df.head())
except FileNotFoundError:
    print("SoLEXS data not found. Please download from PRADAN.")
    solexs_df = pd.DataFrame()
    solexs_gti = []
""",
    """# Expected files from PRADAN portal inside the day's zip:
# lightcurve_cdt1.fits, lightcurve_czt1.fits (and cdte2, czt2)
# gticdte1.fits, gticzt1.fits

helios_data = read_helios_lc_all(HELIOS_DATA_DIR)
helios_gti_cdte = read_helios_gti(HELIOS_DATA_DIR / "gticdte1.fits")
helios_gti_czt = read_helios_gti(HELIOS_DATA_DIR / "gticzt1.fits")

# Show what bands were loaded for CZT1
print("CZT1 bands loaded:")
if 'czt1' in helios_data and helios_data['czt1']:
    for band_name, band_df in helios_data['czt1'].items():
        if not band_df.empty:
            print(f"  {band_name}: {len(band_df)} rows, "
                  f"max={band_df['ctr'].max():.1f} cts/s")
else:
    print("HEL1OS data not found.")
""",
    """merged_df = merge_instruments(
    solexs_lc_sdd1=None,          # skip SDD1 (saturates)
    solexs_lc_sdd2=solexs_df if not solexs_df.empty else None,
    solexs_gti=solexs_gti,
    helios_data=helios_data,
    helios_gti={'cdte1': helios_gti_cdte, 'czt1': helios_gti_czt}
)

if not merged_df.empty:
    print(f"\\nMerged DataFrame shape: {merged_df.shape}")
    print(f"Columns: {list(merged_df.columns)}")
    print(f"\\nData quality distribution:")
    print(merged_df['data_quality'].value_counts().sort_index())
    print(f"\\nDual coverage: {merged_df['data_quality'].ge(7).mean()*100:.1f}%")
    display(merged_df.head(10))
else:
    print("Merged dataframe is empty.")
""",
    """# The M5.0 flare on July 17, 2024 peaked around 06:35 UTC
if not merged_df.empty:
    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
    fig.suptitle('July 17, 2024 — M5.0 Solar Flare\\nAditya-L1 SoLEXS + HEL1OS Combined', 
                 fontsize=14, fontweight='bold')
    
    flare_start = pd.Timestamp('2024-07-17 06:15', tz='UTC')
    flare_end   = pd.Timestamp('2024-07-17 07:00', tz='UTC')
    mask = (merged_df.index >= flare_start) & (merged_df.index <= flare_end)
    df_flare = merged_df[mask]
    
    # Panel 1: SoLEXS soft X-ray
    ax1 = axes[0]
    ax1.semilogy(df_flare.index, df_flare['solexs_sdd2_ctr'], 
                 color='#2196F3', linewidth=1.2, label='SoLEXS SDD2 (2–22 keV)')
    ax1.fill_between(df_flare.index, 
                     df_flare['solexs_sdd2_ctr'] - df_flare['solexs_sdd2_err'],
                     df_flare['solexs_sdd2_ctr'] + df_flare['solexs_sdd2_err'],
                     alpha=0.3, color='#2196F3')
    ax1.set_ylabel('Count Rate\\n(cts/s)', fontsize=10)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_title('Soft X-ray (SoLEXS)', fontsize=10)
    
    # Panel 2: HEL1OS CdTe hard X-ray
    ax2 = axes[1]
    if 'helios_cdte_40_60_ctr' in df_flare.columns:
        ax2.semilogy(df_flare.index, df_flare['helios_cdte_40_60_ctr'], 
                     color='#FF9800', linewidth=1.2, label='CdTe (40–60 keV)')
    if 'helios_cdte_broad_ctr' in df_flare.columns:
        ax2.semilogy(df_flare.index, df_flare['helios_cdte_broad_ctr'], 
                     color='#FF5722', linewidth=0.8, alpha=0.7, label='CdTe broadband')
    ax2.set_ylabel('Count Rate\\n(cts/s)', fontsize=10)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_title('Hard X-ray CdTe (HEL1OS)', fontsize=10)
    
    # Panel 3: HEL1OS CZT (highest energy)
    ax3 = axes[2]
    czt_cols = [c for c in df_flare.columns if 'czt' in c and 'ctr' in c and 'broad' not in c]
    colors = ['#9C27B0', '#673AB7', '#3F51B5', '#1976D2']
    for col, color in zip(czt_cols, colors):
        band_label = col.replace('helios_czt_', '').replace('_ctr', '').replace('_', '–') + ' keV'
        ax3.semilogy(df_flare.index, df_flare[col], 
                     color=color, linewidth=1.0, alpha=0.8, label=band_label)
    ax3.set_ylabel('Count Rate\\n(cts/s)', fontsize=10)
    ax3.legend(loc='upper right', fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_title('Hard X-ray CZT (HEL1OS)', fontsize=10)
    
    # Panel 4: Hardness Ratio (key flare precursor)
    ax4 = axes[3]
    hr = df_flare['hardness_ratio'].rolling(window=5, center=True).median()
    ax4.plot(df_flare.index, hr, color='#E53935', linewidth=1.5, label='Hardness Ratio (HR)')
    ax4.axhline(y=hr.quantile(0.75), color='orange', linestyle='--', alpha=0.7, label='75th percentile')
    ax4.set_ylabel('HR\\n(hard/soft)', fontsize=10)
    ax4.set_xlabel('Time (UTC)', fontsize=10)
    ax4.legend(loc='upper right', fontsize=9)
    ax4.grid(True, alpha=0.3)
    ax4.set_title('Hardness Ratio — Flare Precursor Indicator', fontsize=10)
    
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax4.xaxis.set_major_locator(mdates.MinuteLocator(byminute=range(0,60,5)))
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig('phase1_validation_july17_flare.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("\\n✅ VALIDATION CHECKLIST:")
    sdd2_peak = df_flare['solexs_sdd2_ctr'].idxmax()
    if pd.notna(sdd2_peak):
        print("1. SoLEXS peak near 06:35 UTC? ->", 
              "PASS" if sdd2_peak.strftime('%H:%M') in ['06:33','06:34','06:35','06:36','06:37'] 
              else "CHECK MANUALLY")
    print("2. HEL1OS CZT peak precedes SoLEXS peak (Neupert effect)? (check plot visually)")
    print("3. Hardness ratio rises before SoLEXS peak? (check plot visually)")
    print("4. No zeros in gap regions (only NaN)?",
          "PASS" if not (merged_df[~merged_df['data_quality'].ge(7)]['solexs_sdd2_ctr'] == 0).any()
          else "FAIL — zeros found in gap regions")
""",
    """if not merged_df.empty:
    output_path = Path("../data/processed/merged_20240717.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_merged(merged_df, output_path)
    print(f"Saved merged data to {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")
"""
]

nb['cells'] = [nbf.v4.new_code_cell(cell) for cell in cells]
nbf.write(nb, 'notebooks/phase1_validation.ipynb')
print("Notebook created successfully.")
