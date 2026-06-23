import zipfile
import shutil
import os
from pathlib import Path

def extract_spectral_files(date_str, solexs_dir, helios_dir, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    solexs_zip = list(Path(solexs_dir).glob(f"AL1_SLX_L1_{date_str}_*.zip"))
    helios_zip = list(Path(helios_dir).glob(f"HLS_{date_str}_*.zip"))
    
    if not solexs_zip or not helios_zip:
        print(f"Could not find matching zips for date {date_str}")
        return
        
    print(f"Extracting SoLEXS spectra from {solexs_zip[0].name}...")
    with zipfile.ZipFile(solexs_zip[0], 'r') as z:
        for f in z.namelist():
            # Search for SDD2 Pulse Invariant (.pi) file
            if "SDD2" in f and f.endswith(".pi.gz"):
                print(f"Found: {f}")
                target_path_gz = out_dir / "AL1_SOLEXS_SDD2_L1.pi.gz"
                target_path = out_dir / "AL1_SOLEXS_SDD2_L1.pi"
                with z.open(f) as source, open(target_path_gz, "wb") as target:
                    shutil.copyfileobj(source, target)
                import gzip
                with gzip.open(target_path_gz, 'rb') as f_in:
                    with open(target_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                target_path_gz.unlink() # cleanup
                print(f"Saved -> {target_path}")
                break

    print(f"\\nExtracting HEL1OS spectra from {helios_zip[0].name}...")
    with zipfile.ZipFile(helios_zip[0], 'r') as z:
        for f in z.namelist():
            if "czt_spectra_czt1" in f and f.endswith(".fits"):
                print(f"Found: {f}")
                target_path = out_dir / "hellos_czt1_spectra.fits"
                with z.open(f) as source, open(target_path, "wb") as target:
                    shutil.copyfileobj(source, target)
                print(f"Saved -> {target_path}")
                break

if __name__ == "__main__":
    date = "20240717"
    solexs_dir = "/Users/aditya1981/Downloads/Solex dataset"
    helios_dir = "/Users/aditya1981/Documents/Helios dataset"
    out_dir = "/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed"
    extract_spectral_files(date, solexs_dir, helios_dir, out_dir)
