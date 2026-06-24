import os
import sys
import glob
from pathlib import Path

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from astropy.io import fits
except ImportError:
    print("This script requires 'astropy', 'numpy', and 'matplotlib'.")
    print("Installing them using pip...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "astropy", "numpy", "matplotlib"])
    import numpy as np
    import matplotlib.pyplot as plt
    from astropy.io import fits

def visualize_fits_file(fits_path, output_png_path=None):
    """
    Opens a SUIT FITS file, extracts header metadata, and visualizes the 2D solar disk.
    """
    print(f"\nOpening FITS file: {fits_path}")
    try:
        with fits.open(fits_path) as hdul:
            # Print basic info
            hdul.info()
            
            # The primary HDU or the first image extension contains the data
            # Check where the image data is located
            data_idx = 0
            for idx, hdu in enumerate(hdul):
                if hdu.data is not None and len(hdu.data.shape) == 2:
                    data_idx = idx
                    break
                    
            header = hdul[data_idx].header
            data = hdul[data_idx].data
            
            # Extract header info
            date_obs = header.get('DATE-OBS', 'Unknown')
            wavelength = header.get('WAVELNTH', 'Unknown')
            exptime = header.get('EXPTIME', 'Unknown')
            detector = header.get('DETECTOR', 'SUIT')
            
            print(f"Header Metadata:")
            print(f"  - Observed: {date_obs}")
            print(f"  - Wavelength: {wavelength} Å")
            print(f"  - Exposure Time: {exptime} s")
            print(f"  - Image Dimensions: {data.shape}")
            
            # Plot the image
            plt.figure(figsize=(10, 10))
            
            # Apply a logarithmic scaling to enhance contrast in faint regions
            # if the intensity range is high
            vmin = np.percentile(data, 1)
            vmax = np.percentile(data, 99.5)
            
            # Solar imaging color maps: 'sdoaia171' (gold/yellow), or 'copper'/'inferno'
            cmap = 'inferno' if wavelength != 'Unknown' else 'gray'
            
            plt.imshow(data, cmap=cmap, origin='lower', vmin=vmin, vmax=vmax)
            plt.colorbar(label='Intensity (counts)')
            
            title = f"{detector} Solar Image - {wavelength} Å\nObserved: {date_obs} (Exp: {exptime}s)"
            plt.title(title, fontsize=14, fontweight='bold', pad=15)
            plt.xlabel('X (pixels)')
            plt.ylabel('Y (pixels)')
            
            plt.tight_layout()
            
            if output_png_path:
                plt.savefig(output_png_path, dpi=300, bbox_inches='tight')
                print(f"Saved visual verification plot to: {output_png_path}")
            else:
                plt.show()
                
            plt.close()
            return True
    except Exception as e:
        plt.close()
        print(f"Error reading FITS file: {e}")
        return False

def main():
    print("="*60)
    print("       SUIT FITS Data Visualization & Verification")
    print("="*60)
    
    project_root = Path(__file__).resolve().parent.parent
    suit_dir = project_root / "data" / "raw" / "suit"
    
    fits_files = sorted(glob.glob(str(suit_dir / "*.fits")))
    
    if not fits_files:
        print(f"\nNo FITS files found in {suit_dir.resolve()}.")
        print("Please run scripts/suit_downloader.py first to download some samples.")
        return
        
    print(f"\nFound {len(fits_files)} FITS files.")
    
    for idx, fits_file in enumerate(fits_files):
        base_name = Path(fits_file).stem
        output_png = project_root / "data" / "processed" / f"suit_verification_{base_name}.png"
        output_png.parent.mkdir(parents=True, exist_ok=True)
        
        brain_png = Path(f"/Users/aditya1981/.gemini/antigravity-ide/brain/ead5211d-dfba-45f4-a3a2-adaf18c4ec59/suit_verification_{base_name}.png")
        
        success = visualize_fits_file(fits_file, output_png_path=str(output_png))
        if success:
            import shutil
            try:
                shutil.copy(output_png, brain_png)
                print(f"Copied verification preview to brain: {brain_png}")
            except Exception as e:
                print(f"Could not copy preview to brain: {e}")

if __name__ == "__main__":
    main()
