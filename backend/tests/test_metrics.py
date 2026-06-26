import numpy as np
from aditya_flare.evaluation.metrics import compute_skill_scores, compute_calibration_errors

def test_compute_skill_scores():
    y_true = np.array([1, 1, 0, 0])
    y_pred = np.array([1, 0, 0, 0])
    
    scores = compute_skill_scores(y_true, y_pred)
    assert scores['TP'] == 1
    assert scores['FN'] == 1
    assert scores['FP'] == 0
    assert scores['TN'] == 2
    assert scores['TPR'] == 0.5
    assert scores['FPR'] == 0.0

def test_compute_calibration_errors():
    y_true = np.array([1, 0, 1, 0])
    y_prob = np.array([0.9, 0.1, 0.8, 0.2])
    
    ece, mce = compute_calibration_errors(y_true, y_prob)
    assert ece >= 0
    assert mce >= 0
