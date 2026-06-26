import zipfile
import shutil
import os
from pathlib import Path

date_str = "20240212"
solexs_dir = "/Users/aditya1981/Downloads/Solex dataset"
out_dir = Path("/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed/20240212")
out_dir.mkdir(parents=True, exist_ok=True)

solexs_zip = list(Path(solexs_dir).glob(f"AL1_SLX_L1_{date_str}_*.zip"))
if not solexs_zip:
    print("No SoLEXS ZIP found for 20240212")
else:
    print(f"Extracting SoLEXS spectra from {solexs_zip[0].name}...")
    with zipfile.ZipFile(solexs_zip[0], "r") as z:
        for f in z.namelist():
            if "SDD2" in f and f.endswith(".pi.gz"):
                print(f"Found: {f}")
                target_path_gz = out_dir / "AL1_SOLEXS_SDD2_L1.pi.gz"
                target_path = out_dir / "AL1_SOLEXS_SDD2_L1.pi"
                with z.open(f) as source, open(target_path_gz, "wb") as target:
                    shutil.copyfileobj(source, target)
                import gzip
                with gzip.open(target_path_gz, "rb") as f_in:
                    with open(target_path, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                target_path_gz.unlink() # cleanup
                print(f"Saved -> {target_path}")
                break
