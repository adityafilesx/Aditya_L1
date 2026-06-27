import pytest
import numpy as np
import pandas as pd
from backend.aditya_flare.data.readers.time_utils import (
    unix_to_utc,
    mjd_to_utc,
    utc_to_unix,
    utc_to_mjd,
    align_to_common_grid
)

class TestUnixToUtc:
    def test_known_value(self):
        unix = 1707715800
        result = unix_to_utc(unix)
        expected = pd.Timestamp('2024-02-12T05:30:00', tz='UTC')
        assert result[0] == expected
        
    def test_array_input(self):
        unix = np.array([1707715800, 1707715801, 1707715802])
        result = unix_to_utc(unix)
        assert len(result) == 3
        assert (result[1] - result[0]).total_seconds() == 1.0
        
    def test_july17_flare(self):
        unix = 1721186076
        result = unix_to_utc(unix)
        assert result[0].year == 2024
        assert result[0].month == 7
        assert result[0].day == 17
        assert result[0].hour == 3
        assert result[0].minute == 14

class TestMjdToUtc:
    def test_helios_reference_mjd(self):
        mjd = 60507.99995398406
        result = mjd_to_utc(mjd)
        expected = pd.Timestamp('2024-07-16T23:59:56.024', tz='UTC')
        assert abs((result[0] - expected).total_seconds()) < 0.01
        
    def test_precision(self):
        mjd1 = 60507.99995398406
        mjd2 = mjd1 + 1/86400.0
        result1 = mjd_to_utc(mjd1)
        result2 = mjd_to_utc(mjd2)
        assert abs((result2[0] - result1[0]).total_seconds() - 1.0) < 0.01

class TestRoundTrip:
    def test_unix_roundtrip(self):
        unix_in = np.array([1707715800, 1707802200])
        utc = unix_to_utc(unix_in)
        unix_out = utc_to_unix(utc)
        assert np.allclose(unix_in, unix_out, atol=1)
        
    def test_mjd_roundtrip(self):
        mjd_in = np.array([60507.99995, 60508.5])
        utc = mjd_to_utc(mjd_in)
        mjd_out = utc_to_mjd(utc)
        assert np.allclose(mjd_in, mjd_out, atol=1e-5)

class TestAlignToCommonGrid:
    def test_overlap(self):
        time_a = pd.date_range('2024-07-17 06:00', periods=3600, freq='1s', tz='UTC')
        time_b = pd.date_range('2024-07-17 06:30', periods=3600, freq='1s', tz='UTC')
        result = align_to_common_grid(time_a, time_b)
        assert result.min() >= time_b.min()
        assert result.max() <= time_a.max()
        assert result.freq == pd.tseries.frequencies.to_offset('1s')
        
    def test_no_overlap_raises(self):
        time_a = pd.date_range('2024-07-17 06:00', periods=600, freq='1s', tz='UTC')
        time_b = pd.date_range('2024-07-17 08:00', periods=600, freq='1s', tz='UTC')
        with pytest.raises(ValueError):
            align_to_common_grid(time_a, time_b)
