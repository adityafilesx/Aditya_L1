import os
import sys
import re
import argparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np
from tqdm import tqdm

try:
    import netCDF4
except ImportError:
    print("This script requires 'netCDF4' library. Please run: pip install netCDF4")
    sys.exit(1)

# Base URL for NOAA GOES-R series EXIS Science-quality L1b data
BASE_URL = "https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes"

def get_noaa_directory_url(satellite, year, month):
    """
    Constructs the NCEI directory URL for EXIS science-quality L1b data.
    """
    return f"{BASE_URL}/{satellite}/l1b/exis-l1b-sfxr_science/{year}/{month:02d}/"

def fetch_files_list(session, satellite, date):
    """
    Queries NOAA directory listing for the given date to find matching NetCDF files.
    """
    url = get_noaa_directory_url(satellite, date.year, date.month)
    print(f"Checking NOAA index: {url}")
    
    try:
        response = session.get(url, timeout=15)
        if response.status_code != 200:
            print(f"Warning: Directory not found (HTTP {response.status_code})")
            return []
            
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
    except Exception as e:
        print(f"Error querying NOAA directory: {e}")
        return []
        
    # Standard format: sci_exis-l1b-sfxr_g16_dYYYYMMDD_v0-0-2.nc
    # Note: g16 is GOES-16, g18 is GOES-18
    sat_code = "g16" if "16" in satellite else "g18"
    date_str = date.strftime("%Y%m%d")
    pattern = rf"sci_exis-l1b-sfxr_{sat_code}_d{date_str}_v.*\.nc"
    
    matching_files = []
    for link in links:
        href = link.get("href")
        if href and re.match(pattern, href):
            matching_files.append((href, url + href))
            
    return matching_files

def download_file(session, file_url, dest_path):
    """
    Downloads a single file from the NOAA repository with a progress bar.
    """
    try:
        response = session.get(file_url, stream=True, timeout=30)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        
        with open(dest_path, "wb") as f, tqdm(
            desc=dest_path.name,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    size = f.write(chunk)
                    bar.update(size)
        return True
    except Exception as e:
        print(f"Error downloading {file_url}: {e}")
        if dest_path.exists():
            dest_path.unlink()
        return False

def parse_and_extract_goes_nc(nc_path, output_dir, cadence="1min"):
    """
    Parses the downloaded NetCDF GOES L1b file, extracts variables, and resamples them.
    Saves the extracted dataset as Parquet and CSV.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Parsing raw NetCDF: {nc_path.name}")
    try:
        f = netCDF4.Dataset(nc_path)
    except Exception as e:
        print(f"Error opening NetCDF file {nc_path}: {e}")
        return None
        
    try:
        time_var = f.variables["time"]
        # Retrieve short wavelength channel (0.05-0.4 nm) and long wavelength channel (0.1-0.8 nm)
        # We use irradiance_xrsa1 (minimum channel) and irradiance_xrsb1 (minimum channel) as primary
        xrsa_var = f.variables["irradiance_xrsa1"]
        xrsb_var = f.variables["irradiance_xrsb1"]
        
        time_data = time_var[:]
        xrsa_data = xrsa_var[:]
        xrsb_data = xrsb_var[:]
        
        # Decode times from unit representation (typically "seconds since 2000-01-01 12:00:00")
        time_units = getattr(time_var, "units", "seconds since 2000-01-01 12:00:00")
        times = netCDF4.num2date(time_data, time_units)
        
        # Convert cftime datetime objects to ISO strings and then to pandas DatetimeIndex
        time_strings = [t.isoformat() for t in times]
        df_time = pd.to_datetime(time_strings, utc=True)
        
        # Build pandas DataFrame
        df = pd.DataFrame({
            "goes_xrsa_flux": xrsa_data,
            "goes_xrsb_flux": xrsb_data
        }, index=df_time)
        
        df.index.name = "time_utc"
        
        # Resample to desired cadence (e.g. '1min' or '1s')
        print(f"Resampling to {cadence} cadence...")
        df_resampled = df.resample(cadence).mean()
        
        # Forward fill up to a limit to handle short data gaps
        df_resampled = df_resampled.interpolate(method="linear", limit=10).ffill()
        
        # Save parsed dataset
        date_str = nc_path.name.split("_d")[1].split("_")[0]
        
        parquet_path = output_dir / f"goes_flux_{date_str}.parquet"
        csv_path = output_dir / f"goes_flux_{date_str}.csv"
        
        df_resampled.to_parquet(parquet_path)
        df_resampled.to_csv(csv_path)
        
        print(f"Successfully processed {len(df_resampled)} records.")
        print(f"  Parquet saved: {parquet_path}")
        print(f"  CSV saved: {csv_path}")
        
        # Print summary stats
        print(f"  Short channel (XRSA) - Min: {df_resampled['goes_xrsa_flux'].min():.3e}, Max: {df_resampled['goes_xrsa_flux'].max():.3e}")
        print(f"  Long channel (XRSB)  - Min: {df_resampled['goes_xrsb_flux'].min():.3e}, Max: {df_resampled['goes_xrsb_flux'].max():.3e}")
        
        return df_resampled
    except Exception as e:
        print(f"Error parsing NetCDF data: {e}")
        return None
    finally:
        f.close()

def main():
    parser = argparse.ArgumentParser(description="NOAA GOES-R EXIS XRS Science-Quality Ingestor")
    parser.add_argument("--start", type=str, default="2024-02-12", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2024-02-12", help="End date (YYYY-MM-DD)")
    parser.add_argument("--satellite", type=str, default="goes16", choices=["goes16", "goes18"], help="GOES Satellite identifier")
    parser.add_argument("--dest", type=str, default="data/raw/goes", help="Raw NC file directory")
    parser.add_argument("--extract-dir", type=str, default="data/processed/goes", help="Processed parquet/CSV directory")
    parser.add_argument("--cadence", type=str, default="1min", help="Resampling cadence (e.g. 1s, 10s, 1min)")
    
    args = parser.parse_args()
    
    print("="*60)
    print("     NOAA GOES-R EXIS XRS Solar Flux Ingestor")
    print("="*60)
    
    try:
        start_date = pd.to_datetime(args.start)
        end_date = pd.to_datetime(args.end)
    except Exception as e:
        print(f"Error parsing start/end date: {e}")
        sys.exit(1)
        
    raw_dir = Path(args.dest)
    processed_dir = Path(args.extract_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate list of dates to download
    dates = pd.date_range(start_date, end_date)
    print(f"Preparing to process {len(dates)} day(s) from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} for {args.satellite}...")
    
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    })
    
    total_downloaded = 0
    total_processed = 0
    
    for date in dates:
        print(f"\n--- Processing Date: {date.strftime('%Y-%m-%d')} ---")
        
        # 1. Fetch available files on NOAA server
        files = fetch_files_list(session, args.satellite, date)
        if not files:
            print("No matching science quality files found for this date.")
            continue
            
        # Normally there is one primary science file per day
        for filename, url in files:
            dest_file = raw_dir / filename
            success = True
            
            # 2. Download file
            if dest_file.exists():
                print(f"Raw file {filename} already exists. Skipping download.")
            else:
                print(f"Downloading from NOAA...")
                success = download_file(session, url, dest_file)
                if success:
                    total_downloaded += 1
                    
            # 3. Parse and Extract
            if success:
                df = parse_and_extract_goes_nc(dest_file, processed_dir, args.cadence)
                if df is not None:
                    total_processed += 1
                    
    print("\n" + "="*60)
    print(f"Ingestion Task Completed!")
    print(f"  Downloaded files: {total_downloaded}")
    print(f"  Processed files:  {total_processed}")
    print(f"  Raw directory:    {raw_dir.resolve()}")
    print(f"  Processed dir:    {processed_dir.resolve()}")
    print("="*60)

if __name__ == "__main__":
    main()
