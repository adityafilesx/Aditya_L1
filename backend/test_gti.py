import zipfile
from astropy.io import fits
with zipfile.ZipFile("/Users/aditya1981/Documents/Helios dataset/HLS_20240717_120003_43194sec_lev1_V111.zip", "r") as z:
    z.extract("2024/07/17/HLS_20240717_120003_43194sec_lev1_V111/aux/gticdte1.fits", "/tmp/")
hdul = fits.open("/tmp/2024/07/17/HLS_20240717_120003_43194sec_lev1_V111/aux/gticdte1.fits")
print(hdul[1].columns)
