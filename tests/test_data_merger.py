import pytest
import os
import numpy as np
import pandas as pd
from aditya_flare.data.merger.data_merger import merge_instruments, save_merged, load_merged

@pytest.fixture
def make_fake_solexs_df():
    time_utc = pd.date_range('2024-07-17 06:00', periods=3600, freq='1s', tz='UTC')
    counts = np.sin(np.linspace(0, 10, 3600)) * 50 + 100
    df = pd.DataFrame({
        'time_utc': time_utc,
        'counts': counts,
        'stat_err': np.sqrt(counts),
        'detector': 'SDD2'
    })
    return df

@pytest.fixture
def make_fake_helios_czt_df():
    time_utc = pd.date_range('2024-07-17 06:05', periods=3600, freq='1s', tz='UTC')
    counts = np.sin(np.linspace(0, 10, 3600)) * 20 + 50
    bands = {
        '20.00_TO_40.00_KEV': pd.DataFrame({'time_utc': time_utc, 'ctr': counts, 'stat_err': np.sqrt(counts), 'elow_kev': 20.0, 'ehigh_kev': 40.0}),
        '40.00_TO_60.00_KEV': pd.DataFrame({'time_utc': time_utc, 'ctr': counts*0.8, 'stat_err': np.sqrt(counts*0.8), 'elow_kev': 40.0, 'ehigh_kev': 60.0}),
        '60.00_TO_80.00_KEV': pd.DataFrame({'time_utc': time_utc, 'ctr': counts*0.6, 'stat_err': np.sqrt(counts*0.6), 'elow_kev': 60.0, 'ehigh_kev': 80.0}),
        '80.00_TO_150.00_KEV': pd.DataFrame({'time_utc': time_utc, 'ctr': counts*0.4, 'stat_err': np.sqrt(counts*0.4), 'elow_kev': 80.0, 'ehigh_kev': 150.0}),
        '18.00_TO_160.00_KEV': pd.DataFrame({'time_utc': time_utc, 'ctr': counts*2.8, 'stat_err': np.sqrt(counts*2.8), 'elow_kev': 18.0, 'ehigh_kev': 160.0})
    }
    return {'czt1': bands}

def test_merge_produces_correct_columns(make_fake_solexs_df, make_fake_helios_czt_df):
    solexs_df = make_fake_solexs_df
    helios_data = make_fake_helios_czt_df
    
    merged = merge_instruments(
        solexs_lc_sdd1=None,
        solexs_lc_sdd2=solexs_df,
        solexs_gti=None,
        helios_data=helios_data,
        helios_gti=None
    )
    
    assert 'solexs_sdd2_ctr' in merged.columns
    assert 'hardness_ratio' in merged.columns
    assert 'data_quality' in merged.columns
    assert isinstance(merged.index, pd.DatetimeIndex)
    assert merged.index.tz is not None

def test_nan_in_gaps(make_fake_solexs_df, make_fake_helios_czt_df):
    solexs_df = make_fake_solexs_df
    # Create gap
    solexs_df = pd.concat([solexs_df.iloc[:600], solexs_df.iloc[660:]])
    
    helios_data = make_fake_helios_czt_df
    
    merged = merge_instruments(
        solexs_lc_sdd1=None,
        solexs_lc_sdd2=solexs_df,
        solexs_gti=None,
        helios_data=helios_data,
        helios_gti=None
    )
    
    # Grid should cover the gap. The rows in gap should be NaN for SoLEXS
    gap_times = merged.index[(merged.index > pd.Timestamp('2024-07-17 06:10:00', tz='UTC')) & 
                             (merged.index < pd.Timestamp('2024-07-17 06:10:59', tz='UTC'))]
    assert np.isnan(merged.loc[gap_times, 'solexs_sdd2_ctr']).all()
    # Check that rows in gap are not 0
    assert not (merged.loc[gap_times, 'solexs_sdd2_ctr'] == 0.0).any()

def test_hardness_ratio_not_nan_during_coverage(make_fake_solexs_df, make_fake_helios_czt_df):
    solexs_df = make_fake_solexs_df
    helios_data = make_fake_helios_czt_df
    
    merged = merge_instruments(
        solexs_lc_sdd1=None,
        solexs_lc_sdd2=solexs_df,
        solexs_gti=None,
        helios_data=helios_data,
        helios_gti=None
    )
    
    # Dual coverage is when both have data (from 06:05 to 07:00)
    dual_mask = merged['solexs_sdd2_ctr'].notna() & merged['helios_czt_broad_ctr'].notna()
    assert merged.loc[dual_mask, 'hardness_ratio'].notna().all()
    
    # SoLEXS only (06:00 to 06:05)
    solexs_only_mask = merged['solexs_sdd2_ctr'].notna() & merged['helios_czt_broad_ctr'].isna()
    assert merged.loc[solexs_only_mask, 'hardness_ratio'].isna().all()

def test_data_quality_bitmask(make_fake_solexs_df, make_fake_helios_czt_df):
    solexs_df = make_fake_solexs_df
    helios_data = make_fake_helios_czt_df
    
    merged = merge_instruments(
        solexs_lc_sdd1=None,
        solexs_lc_sdd2=solexs_df,
        solexs_gti=None,
        helios_data=helios_data,
        helios_gti=None
    )
    
    dual_mask = merged['solexs_sdd2_ctr'].notna() & merged['helios_czt_broad_ctr'].notna()
    assert (merged.loc[dual_mask, 'data_quality'] >= 5).all()
    
    solexs_only = merged['solexs_sdd2_ctr'].notna() & merged['helios_czt_broad_ctr'].isna()
    assert (merged.loc[solexs_only, 'data_quality'] & 1).all()
    assert not (merged.loc[solexs_only, 'data_quality'] & 4).any()

def test_save_and_load_roundtrip(make_fake_solexs_df, make_fake_helios_czt_df):
    solexs_df = make_fake_solexs_df
    helios_data = make_fake_helios_czt_df
    
    merged = merge_instruments(
        solexs_lc_sdd1=None,
        solexs_lc_sdd2=solexs_df,
        solexs_gti=None,
        helios_data=helios_data,
        helios_gti=None
    )
    
    path = '/tmp/test_merge.parquet'
    save_merged(merged, path)
    loaded = load_merged(path)
    
    pd.testing.assert_frame_equal(merged, loaded, check_freq=False)
    os.remove(path)
    if os.path.exists('/tmp/test_merge.json'):
        os.remove('/tmp/test_merge.json')
