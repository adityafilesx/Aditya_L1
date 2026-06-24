from astropy.io import fits
from astropy.time import Time
import numpy as np

f = "data/processed/20240212/AL1_SOLEXS_SDD2_L1.pi"
with fits.open(f) as hdul:
    print("Primary Header:")
    for key in ['DATE-OBS', 'TIME-OBS', 'DATE-END', 'TIME-END']:
        if key in hdul[0].header:
            print(f"{key}: {hdul[0].header[key]}")
    
    spec_ext = hdul['SPECTRUM']
    print(f"\nSPECTRUM Header:")
    for key in ['DATE-OBS', 'TIME-OBS', 'DATE-END', 'TIME-END']:
        if key in spec_ext.header:
            print(f"{key}: {spec_ext.header[key]}")
    
    # Try to find time columns in SPECTRUM or GTI
    print(f"\nColumns in SPECTRUM: {spec_ext.columns.names}")
    
    if 'TIME' in spec_ext.columns.names:
        times = spec_ext.data['TIME']
        print(f"Time starts at {times[0]} and ends at {times[-1]}")
    
    # Or maybe it's just bins corresponding to 1s?
    num_spectra = len(spec_ext.data)
    print(f"\nNumber of spectra: {num_spectra}")
