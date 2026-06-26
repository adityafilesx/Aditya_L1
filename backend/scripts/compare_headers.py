from astropy.io import fits
f1 = "data/processed/AL1_SOLEXS_SDD2_L1.pi"
f2 = "data/processed/20240212/AL1_SOLEXS_SDD2_L1.pi"

with fits.open(f1) as hdul1, fits.open(f2) as hdul2:
    h1 = hdul1["SPECTRUM"].header
    h2 = hdul2["SPECTRUM"].header
    print("BACKFILE in old:", h1.get("BACKFILE", "MISSING"))
    print("BACKFILE in new:", h2.get("BACKFILE", "MISSING"))
    
    for k in ["RESPFILE", "ANCRFILE", "STAT_ERR", "SYS_ERR", "POISSERR", "GROUPING", "QUALITY"]:
        print(f"{k} old: {h1.get(k, 'MISSING')}, new: {h2.get(k, 'MISSING')}")
