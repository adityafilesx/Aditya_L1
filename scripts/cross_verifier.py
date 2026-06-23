import argparse
from pathlib import Path
import re
import json
import pandas as pd

def parse_solexs_date(filename):
    match = re.search(r'AL1_SLX_L1_(\d{8})_', filename)
    if match:
        return match.group(1)
    return None

def parse_helios_date(filename):
    match = re.search(r'HLS_(\d{8})_', filename)
    if match:
        return match.group(1)
    return None

def main():
    parser = argparse.ArgumentParser(description='Cross-verify processed Aditya-L1 data against raw zip archives.')
    parser.add_argument('--solexs-dir', type=str, default='/Users/aditya1981/Downloads/Solex dataset', help='Path to SoLEXS zip files')
    parser.add_argument('--helios-dir', type=str, default='/Users/aditya1981/Documents/Helios dataset', help='Path to HEL1OS zip files')
    parser.add_argument('--processed-dir', type=str, default='../data/processed', help='Path to processed parquet files')
    
    args = parser.parse_args()
    
    # Adjust relative paths
    if args.processed_dir == '../data/processed':
        args.processed_dir = Path(__file__).resolve().parent.parent / 'data' / 'processed'
    else:
        args.processed_dir = Path(args.processed_dir)
        
    solexs_dir = Path(args.solexs_dir)
    helios_dir = Path(args.helios_dir)
    
    # 1. Identify expected dates from raw zips
    solexs_dates = set()
    helios_dates = set()
    
    if solexs_dir.exists():
        for f in solexs_dir.glob('AL1_SLX_L1_*.zip'):
            date = parse_solexs_date(f.name)
            if date:
                solexs_dates.add(date)
                
    if helios_dir.exists():
        for f in helios_dir.glob('HLS_*.zip'):
            date = parse_helios_date(f.name)
            if date:
                helios_dates.add(date)
                
    expected_dates = sorted(list(solexs_dates & helios_dates))
    
    # 2. Identify actual processed dates
    processed_dates = set()
    metadata_stats = []
    
    if args.processed_dir.exists():
        for f in args.processed_dir.glob('merged_*.parquet'):
            match = re.search(r'merged_(\d{8})\.parquet', f.name)
            if match:
                date = match.group(1)
                processed_dates.add(date)
                
                # Try to load corresponding JSON for stats
                json_path = f.with_suffix('.json')
                if json_path.exists():
                    try:
                        with open(json_path, 'r') as jf:
                            meta = json.load(jf)
                            meta['date'] = date
                            metadata_stats.append(meta)
                    except:
                        pass

    # 3. Compute discrepancies
    missing_dates = sorted(list(set(expected_dates) - processed_dates))
    extra_dates = sorted(list(processed_dates - set(expected_dates)))
    
    # 4. Report
    print("=" * 60)
    print("ADITYA-L1 DATA INGESTION: CROSS VERIFICATION REPORT")
    print("=" * 60)
    print(f"Raw SoLEXS available dates : {len(solexs_dates)}")
    print(f"Raw HEL1OS available dates : {len(helios_dates)}")
    print(f"Intersection (Expected)    : {len(expected_dates)}")
    print(f"Successfully Processed     : {len(processed_dates)}")
    print("-" * 60)
    
    if missing_dates:
        print(f"\\nWARNING: {len(missing_dates)} expected dates were NOT processed:")
        for md in missing_dates:
            print(f"  - {md}")
    else:
        print("\\nSUCCESS: All expected intersecting dates were successfully processed!")
        
    if extra_dates:
        print(f"\\nNOTE: Found {len(extra_dates)} extra processed dates (not in current raw folders):")
        for ed in extra_dates:
            print(f"  - {ed}")

    if metadata_stats:
        df = pd.DataFrame(metadata_stats)
        if 'dual_coverage_pct' in df.columns:
            avg_cov = df['dual_coverage_pct'].mean()
            print(f"\\nAverage Dual-Instrument Coverage: {avg_cov:.2f}% across {len(df)} days.")
        
        if 'n_seconds' in df.columns:
            total_time = df['n_seconds'].sum() / 3600 # hours
            print(f"Total Combined Observation Time : {total_time:.2f} hours.")
            
    print("=" * 60)

if __name__ == '__main__':
    main()
