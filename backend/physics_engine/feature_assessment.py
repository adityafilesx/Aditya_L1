import numpy as np
import pandas as pd
import logging
import json
from pathlib import Path
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy.stats import pearsonr
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)

def calculate_vif(df: pd.DataFrame, features: list) -> dict:
    """ Calculates Variance Inflation Factor (VIF) to detect multicollinearity. """
    vif_data = {}
    X = df[features].dropna()
    if len(X) < 10: return vif_data
    
    # Add constant for VIF calculation
    X['const'] = 1
    
    for i, col in enumerate(X.columns):
        if col == 'const': continue
        try:
            vif = variance_inflation_factor(X.values, i)
            vif_data[col] = float(vif)
        except Exception:
            vif_data[col] = -1.0
    return vif_data

def calculate_stability(series: pd.Series) -> float:
    return float(series.mean() / (series.std() + 1e-9))

def assess_advanced_importance(df: pd.DataFrame, target_col: str, feature_cols: list):
    X = df[feature_cols].fillna(0)
    y = df[target_col]
    
    if len(np.unique(y)) < 2:
        return {col: {'mutual_information': 0.0, 'permutation_importance_mean': 0.0, 'rfe_rank': -1} for col in feature_cols}
        
    mi = mutual_info_classif(X, y)
    
    rf = RandomForestClassifier(n_estimators=50, random_state=42)
    rf.fit(X, y)
    perm = permutation_importance(rf, X, y, n_repeats=5, random_state=42)
    
    rfe = RFE(estimator=rf, n_features_to_select=max(1, len(feature_cols)//2))
    rfe.fit(X, y)
    
    importance_dict = {}
    for i, col in enumerate(feature_cols):
        importance_dict[col] = {
            'mutual_information': float(mi[i]),
            'permutation_importance_mean': float(perm.importances_mean[i]),
            'rfe_rank': int(rfe.ranking_[i])
        }
    return importance_dict

def generate_feature_report(df: pd.DataFrame, target_col: str, feature_cols: list, out_path: str = "Feature_Quality_Report.json"):
    vif_dict = calculate_vif(df, feature_cols)
    adv_dict = assess_advanced_importance(df, target_col, feature_cols)
    
    report = {}
    for col in feature_cols:
        report[col] = {
            'vif': vif_dict.get(col, -1),
            'stability': calculate_stability(df[col]),
            'mutual_information': adv_dict[col]['mutual_information'],
            'permutation_importance': adv_dict[col]['permutation_importance_mean'],
            'rfe_rank': adv_dict[col]['rfe_rank']
        }
        
    with open(out_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    return report
