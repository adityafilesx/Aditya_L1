import sys
import os
import re
import argparse
import tempfile
import zipfile
import shutil
from pathlib import Path
from tqdm import tqdm
import pandas as pd

# Add project root to path so we can import modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.aditya_flare.data.readers.solexs_reader import read_solexs_lc, read_solexs_gti
from backend.aditya_flare.data.readers.helios_reader import read_helios_lc_all, read_helios_gti
from backend.aditya_flare.data.merger.data_merger import merge_instruments, save_merged

def parse_solexs_date(filename):
    # AL1_SLX_L1_20240201_v1.0.zip -> 20240201
    match = re.search(r'AL1_SLX_L1_(\d{8})_', filename)
    if match:
        return match.group(1)
    return None

def parse_helios_date(filename):
    # HLS_20240701_000211_43057sec_lev1_V311.zip -> 20240701
    match = re.search(r'HLS_(\d{8})_', filename)
    if match:
        return match.group(1)
    return None

def find_matching_dates(solexs_dir, helios_dir):
    solexs_dates = {}
    helios_dates = {}
    
    solexs_dir = Path(solexs_dir)
    helios_dir = Path(helios_dir)
    
    if solexs_dir.exists():
        for f in solexs_dir.glob('AL1_SLX_L1_*.zip'):
            date = parse_solexs_date(f.name)
            if date:
                solexs_dates[date] = f
                
    if helios_dir.exists():
        for f in helios_dir.glob('HLS_*.zip'):
            date = parse_helios_date(f.name)
            if date:
                helios_dates[date] = f
                
    common_dates = sorted(list(set(solexs_dates.keys()) & set(helios_dates.keys())))
    return common_dates, solexs_dates, helios_dates

def process_date(date_str, solexs_zip, helios_zip, output_dir):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        solexs_tmp = tmp_path / 'solexs'
        helios_tmp = tmp_path / 'helios'
        solexs_tmp.mkdir()
        helios_tmp.mkdir()
        
        try:
            # Extract SoLEXS
            with zipfile.ZipFile(solexs_zip, 'r') as z:
                # We only need SDD2 files, and avoid extracting everything to save time/space
                for info in z.infolist():
                    if 'SDD2_L1.lc' in info.filename or 'SDD2_L1.gti' in info.filename:
                        z.extract(info, solexs_tmp)
                        
            # Extract HEL1OS
            with zipfile.ZipFile(helios_zip, 'r') as z:
                # We need lightcurve and gti files
                for info in z.infolist():
                    if 'lightcurve_' in info.filename or 'gti' in info.filename:
                        z.extract(info, helios_tmp)
        except zipfile.BadZipFile:
            print(f"Error: Bad zip file for {date_str}. Skipping.")
            return False
            
        # Locate SoLEXS files
        solexs_lc_files = list(solexs_tmp.rglob('*SDD2_L1.lc*'))
        solexs_gti_files = list(solexs_tmp.rglob('*SDD2_L1.gti*'))
        
        solexs_df = pd.DataFrame()
        solexs_gti = None
        if solexs_lc_files:
            try:
                solexs_df = read_solexs_lc(solexs_lc_files[0])
            except Exception as e:
                print(f"Error reading SoLEXS LC for {date_str}: {e}")
                
        if solexs_gti_files:
            try:
                solexs_gti = read_solexs_gti(solexs_gti_files[0])
            except Exception as e:
                print(f"Error reading SoLEXS GTI for {date_str}: {e}")
                
        # Load HEL1OS
        try:
            helios_data = read_helios_lc_all(helios_tmp)
        except Exception as e:
            print(f"Error reading HEL1OS data for {date_str}: {e}")
            helios_data = {}
            
        helios_gti_cdte = None
        helios_gti_czt = None
        cdte_gti_file = list(helios_tmp.rglob('gticdte1.fits*'))
        if cdte_gti_file:
            try:
                helios_gti_cdte = read_helios_gti(cdte_gti_file[0])
            except:
                pass
        czt_gti_file = list(helios_tmp.rglob('gticzt1.fits*'))
        if czt_gti_file:
            try:
                helios_gti_czt = read_helios_gti(czt_gti_file[0])
            except:
                pass
            
        helios_gti_dict = {}
        if helios_gti_cdte is not None:
            helios_gti_dict['cdte1'] = helios_gti_cdte
        if helios_gti_czt is not None:
            helios_gti_dict['czt1'] = helios_gti_czt
            
        # Merge
        try:
            merged_df = merge_instruments(
                solexs_lc_sdd1=None,
                solexs_lc_sdd2=solexs_df if not solexs_df.empty else None,
                solexs_gti=solexs_gti,
                helios_data=helios_data,
                helios_gti=helios_gti_dict
            )
        except Exception as e:
            print(f"Error merging instruments for {date_str}: {e}")
            return False
        
        if merged_df.empty:
            print(f"No valid data merged for {date_str}")
            return False
            
        output_path = Path(output_dir) / f"merged_{date_str}.parquet"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_merged(merged_df, output_path)
        return True

def main():
    parser = argparse.ArgumentParser(description='Batch ingestion pipeline for Aditya-L1 data')
    parser.add_argument('--solexs-dir', type=str, default=os.path.expanduser('~/Downloads/Solex dataset'), help='Path to SoLEXS zip files')
    parser.add_argument('--helios-dir', type=str, default=os.path.expanduser('~/Documents/Helios dataset'), help='Path to HEL1OS zip files')
    parser.add_argument('--output-dir', type=str, default='../data/processed', help='Path to save merged parquet files')
    parser.add_argument('--dry-run', action='store_true', help='Only show matching dates, do not process')
    parser.add_argument('--date', type=str, help='Process a specific date YYYYMMDD')
    parser.add_argument('--limit', type=int, help='Limit number of files to process')
    
    args = parser.parse_args()
    
    # Adjust output_dir relative to the script if it's a relative path starting with '..'
    if args.output_dir == '../data/processed':
        args.output_dir = str(Path(__file__).resolve().parent.parent / 'data' / 'processed')
    
    print(f"Scanning directories...")
    print(f"SoLEXS: {args.solexs_dir}")
    print(f"HEL1OS: {args.helios_dir}")
    
    common_dates, solexs_map, helios_map = find_matching_dates(args.solexs_dir, args.helios_dir)
    
    if args.date:
        if args.date in common_dates:
            common_dates = [args.date]
        else:
            print(f"Date {args.date} not found in both datasets.")
            print(f"  SoLEXS has this date: {args.date in solexs_map}")
            print(f"  HEL1OS has this date: {args.date in helios_map}")
            return
            
    if args.limit and len(common_dates) > args.limit:
        common_dates = common_dates[:args.limit]
        
    print(f"Found {len(common_dates)} matching dates to process.")
    
    if args.dry_run:
        print("Dry run mode. Dates to process:")
        for d in common_dates:
            print(f"  - {d}")
        return
        
    success_count = 0
    for date in tqdm(common_dates, desc="Processing dates"):
        print(f"\\n--- Processing {date} ---")
        try:
            success = process_date(date, solexs_map[date], helios_map[date], args.output_dir)
            if success:
                success_count += 1
        except Exception as e:
            print(f"Failed processing {date}: {e}")
            import traceback
            traceback.print_exc()
            
    print(f"\\nBatch processing complete. Successfully merged {success_count} / {len(common_dates)} days.")
    print(f"Outputs saved to: {args.output_dir}")

if __name__ == '__main__':
    main()
