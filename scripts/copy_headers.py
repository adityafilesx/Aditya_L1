from astropy.io import fits

f1 = "data/processed/AL1_SOLEXS_SDD2_L1.pi"
f2 = "data/processed/20240212/AL1_SOLEXS_SDD2_L1.pi"

with fits.open(f1) as hdul1, fits.open(f2, mode='update') as hdul2:
    h1 = hdul1["SPECTRUM"].header
    ext2 = hdul2["SPECTRUM"]
    
    # Copy missing keywords from f1 to f2
    for key in h1.keys():
        if key not in ext2.header and key not in ['NAXIS1', 'NAXIS2', 'PCOUNT', 'GCOUNT', 'TFIELDS', 'EXTNAME', 'XTENSION', 'BITPIX', 'NAXIS', 'TTYPE1', 'TFORM1', 'TTYPE2', 'TFORM2', 'TTYPE3', 'TFORM3', 'TTYPE4', 'TFORM4', 'TTYPE5', 'TFORM5', 'TTYPE6', 'TFORM6']:
            ext2.header[key] = h1[key]
            
    hdul2.flush()
    print("Copied all missing keywords from the old .pi file to the new one.")
