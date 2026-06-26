from astropy.io import fits

f = "data/processed/20240212/AL1_SOLEXS_SDD2_L1.pi"
with fits.open(f, mode='update') as hdul:
    ext = hdul['SPECTRUM']
    ext.header['BACKFILE'] = 'NONE'
    ext.header['RESPFILE'] = 'NONE'
    ext.header['ANCRFILE'] = 'NONE'
    ext.header['POISSERR'] = True
    ext.header['STAT_ERR'] = 0
    ext.header['SYS_ERR'] = 0
    hdul.flush()
    print("Patched headers in", f)
