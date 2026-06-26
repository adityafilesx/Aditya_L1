import glob
import re
from pathlib import Path
import pandas as pd
import numpy as np

def main():
    print("="*60)
    print("      Aditya-L1 SoLEXS & NOAA GOES Dataset Aligner")
    print("="*60)
    
    processed_dir = Path("data/processed")
    goes_dir = processed_dir / "goes"
    
    # Scan for processed GOES files
    goes_files = sorted(list(goes_dir.glob("goes_flux_*.parquet")))
    print(f"Found {len(goes_files)} processed GOES daily files.")
    
    aligned_dfs = []
    
    for g_file in goes_files:
        # Extract date string
        # e.g., goes_flux_20240212.parquet -> 20240212
        date_match = re.search(r'goes_flux_(\d{8})\.parquet', g_file.name)
        if not date_match:
            continue
        date_str = date_match.group(1)
        
        # Locate corresponding telemetry file
        telemetry_file = processed_dir / f"merged_{date_str}.parquet"
        if not telemetry_file.exists():
            print(f"Warning: Telemetry file merged_{date_str}.parquet not found. Skipping.")
            continue
            
        print(f"Aligning date: {date_str} ...")
        
        try:
            df_goes = pd.read_parquet(g_file)
            df_tel = pd.read_parquet(telemetry_file)
            
            # Basic validation
            if df_goes.empty or df_tel.empty:
                print(f"  Empty dataframe encountered for {date_str}. Skipping.")
                continue
                
            # Keep index in DatetimeIndex format
            df_goes.index = pd.to_datetime(df_goes.index, utc=True)
            df_tel.index = pd.to_datetime(df_tel.index, utc=True)
            
            # Resample telemetry to 1-minute cadence to match GOES cadence
            # Keep SDD2, SDD1, and hardness ratio
            agg_funcs = {
                'solexs_sdd2_ctr': 'mean',
                'solexs_sdd1_ctr': 'mean',
                'hardness_ratio': 'mean',
                'solexs_in_gti': 'max'
            }
            agg_cols = {k: v for k, v in agg_funcs.items() if k in df_tel.columns}
            df_tel_min = df_tel.resample('1min').agg(agg_cols).interpolate(method='linear', limit=10).ffill()
            
            # Perform asof join (nearest timestamp within 30 seconds)
            df_aligned = pd.merge_asof(
                df_tel_min.sort_index(),
                df_goes.sort_index(),
                left_index=True,
                right_index=True,
                direction='nearest',
                tolerance=pd.Timedelta('30s')
            )
            
            # Drop rows where we have no telemetry or no GOES flux (e.g. outside tracking range)
            df_aligned = df_aligned.dropna(subset=['solexs_sdd2_ctr', 'goes_xrsb_flux'])
            
            if not df_aligned.empty:
                aligned_dfs.append(df_aligned)
                print(f"  Aligned {len(df_aligned)} rows successfully.")
            else:
                print(f"  No overlapping records found for {date_str}.")
        except Exception as e:
            print(f"  Error aligning date {date_str}: {e}")
            
    if not aligned_dfs:
        print("\nError: No aligned dataframes could be constructed.")
        return
        
    # Concatenate all datasets
    full_df = pd.concat(aligned_dfs).sort_index()
    
    # Save the consolidated dataset
    out_file = processed_dir / "aligned_goes_solexs.parquet"
    full_df.to_parquet(out_file)
    
    print("\n" + "="*60)
    print("Dataset Alignment Complete!")
    print(f"  Consolidated Parquet: {out_file.resolve()}")
    print(f"  Total records:         {len(full_df)}")
    print(f"  Datetime range:        {full_df.index.min()} to {full_df.index.max()}")
    
    # Calculate Correlation
    log_solexs = np.log10(full_df['solexs_sdd2_ctr'].replace(0, np.nan))
    log_goes = np.log10(full_df['goes_xrsb_flux'].replace(0, np.nan))
    corr = log_solexs.corr(log_goes)
    
    print(f"  Correlation (Log10 space) between SoLEXS SDD2 and GOES XRSB: {corr:.4f}")
    print("="*60)

if __name__ == "__main__":
    main()
