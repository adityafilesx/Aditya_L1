import numpy as np
from aditya_flare.calibration.calibration_utils import flux_to_goes_class_string, parse_goes_class_string
from aditya_flare.calibration.goes_calibrator import GoesCalibrator

def test_flux_to_goes_class_string():
    assert flux_to_goes_class_string(1.5e-4) == "X1.5"
    assert flux_to_goes_class_string(3.2e-5) == "M3.2"
    assert flux_to_goes_class_string(1.0e-6) == "C1.0"
    assert flux_to_goes_class_string(5.5e-7) == "B5.5"
    assert flux_to_goes_class_string(0) == "Unknown"

def test_parse_goes_class_string():
    assert np.isclose(parse_goes_class_string("X1.5"), 1.5e-4)
    assert np.isclose(parse_goes_class_string("M3.2"), 3.2e-5)
    assert np.isnan(parse_goes_class_string("Invalid"))

def test_goes_calibrator():
    calibrator = GoesCalibrator()
    # Test that minimal counts returns an A class flux
    flux = calibrator.counts_to_flux(0)
    assert flux == 1e-9
    
    flux_1000 = calibrator.counts_to_flux(1000)
    assert flux_1000 > 1e-9
