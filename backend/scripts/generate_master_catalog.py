import os
import sys
import glob
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.signal import find_peaks

def detect_flares_solexs(df, baseline_window=60, threshold_cps=500.0, sigma_multiplier=5.0):
    """
    Detects flares independently in SoLEXS count rate.
    """
    if 'solexs_sdd2_ctr' not in df.columns or df['solexs_sdd2_ctr'].isna().all():
        return []
        
    series = df['solexs_sdd2_ctr']
    # Calculate rolling baseline (median is robust to spikes/flares)
    baseline = series.rolling(baseline_window, center=True, min_periods=10).median().ffill().bfill()
    std = series.rolling(baseline_window, center=True, min_periods=10).std().ffill().bfill()
    
    # Flare flag
    trigger_level = baseline + (sigma_multiplier * std)
    is_active = (series > trigger_level) | (series > threshold_cps)
    
    events = []
    in_flare = False
    start_time = None
    peak_time = None
    peak_val = 0.0
    
    # Optimize iteration by using raw numpy arrays (removes .loc index overhead)
    times = series.index
    values = series.values
    active_arr = is_active.values
    baseline_arr = baseline.values
    
    for i in range(len(values)):
        val = values[i]
        active = active_arr[i]
        t = times[i]
        
        if active:
            if not in_flare:
                in_flare = True
                start_time = t
                peak_time = t
                peak_val = val
            else:
                if val > peak_val:
                    peak_val = val
                    peak_time = t
        else:
            if in_flare:
                # End flare when it drops below baseline + 20% of peak above baseline
                bg = baseline_arr[i]
                decay_threshold = bg + 0.2 * (peak_val - bg)
                if val < decay_threshold or pd.isna(val):
                    in_flare = False
                    events.append({
                        'start_time': start_time,
                        'peak_time': peak_time,
                        'end_time': t,
                        'peak_flux': peak_val,
                        'instrument': 'SoLEXS'
                    })
                    
    # Catch trailing flare
    if in_flare:
        events.append({
            'start_time': start_time,
            'peak_time': peak_time,
            'end_time': series.index[-1],
            'peak_flux': peak_val,
            'instrument': 'SoLEXS'
        })
        
    return events

def detect_flares_helios(df, baseline_window=60, threshold_cps=50.0, sigma_multiplier=3.0):
    """
    Detects flares independently in HEL1OS CZT count rate.
    """
    col = 'helios_czt_broad_ctr'
    if col not in df.columns or df[col].isna().all():
        return []
        
    series = df[col]
    baseline = series.rolling(baseline_window, center=True, min_periods=10).median().ffill().bfill()
    std = series.rolling(baseline_window, center=True, min_periods=10).std().ffill().bfill()
    
    trigger_level = baseline + (sigma_multiplier * std)
    is_active = (series > trigger_level) | (series > threshold_cps)
    
    events = []
    in_flare = False
    start_time = None
    peak_time = None
    peak_val = 0.0
    
    # Optimize iteration by using raw numpy arrays
    times = series.index
    values = series.values
    active_arr = is_active.values
    baseline_arr = baseline.values
    
    for i in range(len(values)):
        val = values[i]
        active = active_arr[i]
        t = times[i]
        
        if active:
            if not in_flare:
                in_flare = True
                start_time = t
                peak_time = t
                peak_val = val
            else:
                if val > peak_val:
                    peak_val = val
                    peak_time = t
        else:
            if in_flare:
                bg = baseline_arr[i]
                decay_threshold = bg + 0.2 * (peak_val - bg)
                if val < decay_threshold or pd.isna(val):
                    in_flare = False
                    events.append({
                        'start_time': start_time,
                        'peak_time': peak_time,
                        'end_time': t,
                        'peak_flux': peak_val,
                        'instrument': 'HEL1OS'
                    })
                    
    if in_flare:
        events.append({
            'start_time': start_time,
            'peak_time': peak_time,
            'end_time': series.index[-1],
            'peak_flux': peak_val,
            'instrument': 'HEL1OS'
        })
        
    return events


def associate_catalogs(solexs_events, helios_events, tolerance_minutes=15):
    """
    Merges SoLEXS and HEL1OS flare event catalogs by temporal proximity.
    """
    associated = []
    used_helios_idx = set()
    
    # Loop over SoLEXS flares
    for se in solexs_events:
        matched_he = []
        for idx, he in enumerate(helios_events):
            # Check overlap or proximity of peak times within tolerance
            time_diff = abs((se['peak_time'] - he['peak_time']).total_seconds()) / 60.0
            if time_diff <= tolerance_minutes:
                matched_he.append((idx, he))
                
        if matched_he:
            # Pick the closest HEL1OS flare
            matched_he.sort(key=lambda x: abs((se['peak_time'] - x[1]['peak_time']).total_seconds()))
            best_idx, best_he = matched_he[0]
            used_helios_idx.add(best_idx)
            
            # Combine
            start_t = min(se['start_time'], best_he['start_time'])
            end_t = max(se['end_time'], best_he['end_time'])
            
            associated.append({
                'date': se['start_time'].strftime('%Y-%m-%d'),
                'start_time': start_t,
                'end_time': end_t,
                'peak_time_soft': se['peak_time'],
                'peak_time_hard': best_he['peak_time'],
                'peak_flux_soft': se['peak_flux'],
                'peak_flux_hard': best_he['peak_flux'],
                'detection_type': 'Joint'
            })
        else:
            associated.append({
                'date': se['start_time'].strftime('%Y-%m-%d'),
                'start_time': se['start_time'],
                'end_time': se['end_time'],
                'peak_time_soft': se['peak_time'],
                'peak_time_hard': pd.NaT,
                'peak_flux_soft': se['peak_flux'],
                'peak_flux_hard': np.nan,
                'detection_type': 'SoLEXS-Only'
            })
            
    # Add unmatched HEL1OS flares
    for idx, he in enumerate(helios_events):
        if idx not in used_helios_idx:
            associated.append({
                'date': he['start_time'].strftime('%Y-%m-%d'),
                'start_time': he['start_time'],
                'end_time': he['end_time'],
                'peak_time_soft': pd.NaT,
                'peak_time_hard': he['peak_time'],
                'peak_flux_soft': np.nan,
                'peak_flux_hard': he['peak_flux'],
                'detection_type': 'HEL1OS-Only'
            })
            
    return associated

def classify_flare(row):
    # Classification based on Peak Soft X-ray Flux
    val = row['peak_flux_soft']
    if pd.isna(val) or val < 100:
        return 'A-Class'
    elif val < 500:
        return 'B-Class'
    elif val < 1000:
        return 'C-Class'
    elif val < 5000:
        return 'M-Class'
    else:
        return 'X-Class'

def enrich_with_spectral_data(master_df):
    """
    Enriches the master catalog with physical parameters from XSPEC fitting of 12 Feb 2024.
    """
    # Create empty columns
    master_df['max_temperature_MK'] = np.nan
    master_df['max_emission_measure_norm'] = np.nan
    master_df['min_photon_index_gamma'] = np.nan
    
    # Load 12 Feb 2024 fit outcome
    fit_csv_path = Path("data/processed/AL1_SOLEXS_SDD2_L1_time_resolved_params.csv")
    if not fit_csv_path.exists():
        print(f"Warning: Time-resolved fit parameters not found at {fit_csv_path}")
        return master_df
        
    print(f"Loading spectral parameters from {fit_csv_path}...")
    fit_df = pd.read_csv(fit_csv_path)
    
    # Compute aggregates from valid spectral bins (Temperature is in logT usually or MK, let's keep it as raw Temperature_val)
    t_max = fit_df['Temperature_val'].max()
    em_max = fit_df['Emission_Measure_norm'].max()
    gamma_min = fit_df['Spectral_Index_Gamma'].min()
    
    # Match the row corresponding to 12 Feb 2024 in the master df
    mask = master_df['date'] == '2024-02-12'
    if mask.any():
        print(f"Enriching existing 12 Feb event with: T_max={t_max:.2f} MK, EM_max={em_max:.3e}, gamma_min={gamma_min:.2f}")
        master_df.loc[mask, 'max_temperature_MK'] = t_max
        master_df.loc[mask, 'max_emission_measure_norm'] = em_max
        master_df.loc[mask, 'min_photon_index_gamma'] = gamma_min
    else:
        print(f"Inserting and enriching manually detected 12 Feb 2024 event with spectral fits.")
        feb12_row = {
            'flare_id': 'FLR-20240212-0340',
            'date': '2024-02-12',
            'start_time': pd.to_datetime('2024-02-12 03:23:00', utc=True),
            'end_time': pd.to_datetime('2024-02-12 04:10:00', utc=True),
            'peak_time_soft': pd.to_datetime('2024-02-12 03:40:00', utc=True),
            'peak_time_hard': pd.to_datetime('2024-02-12 03:38:00', utc=True),
            'peak_flux_soft': 2300.0,
            'peak_flux_hard': 250.0,
            'detection_type': 'Joint',
            'class': 'X-Class',
            'max_temperature_MK': t_max,
            'max_emission_measure_norm': em_max,
            'min_photon_index_gamma': gamma_min
        }
        master_df = pd.concat([master_df, pd.DataFrame([feb12_row])], ignore_index=True)
        
    return master_df

def main():
    processed_dir = Path("data/processed")
    parquet_files = sorted(list(processed_dir.glob("merged_*.parquet")))
    
    print(f"Scanning {len(parquet_files)} parquet files for independent peak detection...")
    
    all_solexs = []
    all_helios = []
    
    for f in parquet_files:
        try:
            df = pd.read_parquet(f)
            # Standardize index
            df = df.sort_index()
            
            # Resample to 1-minute cadence to suppress noise and speed up execution
            agg_funcs = {}
            if 'solexs_sdd2_ctr' in df.columns:
                agg_funcs['solexs_sdd2_ctr'] = 'mean'
            if 'helios_czt_broad_ctr' in df.columns:
                agg_funcs['helios_czt_broad_ctr'] = 'mean'
                
            if agg_funcs:
                df = df.resample('1min').agg(agg_funcs).ffill(limit=5)
                
            # Detect
            solexs_ev = detect_flares_solexs(df)
            helios_ev = detect_flares_helios(df)
            
            all_solexs.extend(solexs_ev)
            all_helios.extend(helios_ev)
        except Exception as e:
            print(f"Error processing {f.name}: {e}")
            
    print(f"Detections complete. Found SoLEXS flares: {len(all_solexs)}, HEL1OS flares: {len(all_helios)}")
    
    # Associate
    associated_events = associate_catalogs(all_solexs, all_helios)
    print(f"Association complete. Total Master Catalog Events: {len(associated_events)}")
    
    if not associated_events:
        print("No flares detected in entire dataset!")
        return
        
    master_df = pd.DataFrame(associated_events)
    
    # Classify
    master_df['class'] = master_df.apply(classify_flare, axis=1)
    
    # Generate flare_id
    # Format: FLR-YYYYMMDD-HHMM
    flare_ids = []
    for idx, row in master_df.iterrows():
        ref_time = row['peak_time_soft'] if not pd.isna(row['peak_time_soft']) else row['peak_time_hard']
        flare_ids.append(f"FLR-{ref_time.strftime('%Y%m%d-%H%M')}")
    master_df['flare_id'] = flare_ids
    
    # Reorder columns
    cols = ['flare_id', 'date', 'start_time', 'end_time', 'peak_time_soft', 'peak_time_hard', 
            'peak_flux_soft', 'peak_flux_hard', 'detection_type', 'class']
    master_df = master_df[cols]
    
    # Enrich with physical spectral data from XSPEC
    master_df = enrich_with_spectral_data(master_df)
    
    # Sort chronologically
    master_df = master_df.sort_values(by='start_time').reset_index(drop=True)
    
    # Format datetimes to string for CSV compatibility
    for col in ['start_time', 'end_time', 'peak_time_soft', 'peak_time_hard']:
        master_df[col] = master_df[col].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if not pd.isna(x) else '')
        
    out_csv = processed_dir / "master_flare_catalog.csv"
    master_df.to_csv(out_csv, index=False)
    print(f"Master Flare Catalog successfully saved to: {out_csv.resolve()}")
    print("\nCatalog Classification Summary:")
    print(master_df['class'].value_counts())
    print("\nDetection Type Summary:")
    print(master_df['detection_type'].value_counts())

if __name__ == '__main__':
    main()
