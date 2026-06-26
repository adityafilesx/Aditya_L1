import pandas as pd
import numpy as np
import logging
from sklearn.metrics import accuracy_score, precision_score, recall_score, brier_score_loss, confusion_matrix
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from pathlib import Path

logger = logging.getLogger(__name__)

def evaluate_physics_improvement(base_df: pd.DataFrame, physics_df: pd.DataFrame, target_col: str = 'is_flare', report_dir: str = "docs/"):
    """
    Trains a quick LightGBM model on baseline features vs physics-enriched features to calculate
    HSS, TSS, Brier Score and measure the improvement.
    """
    logger.info("Evaluating Physics Improvements...")
    
    # We simulate the target if not present for validation purposes
    if target_col not in base_df.columns:
        base_df[target_col] = (base_df['solexs_sdd2_ctr'] > 100.0).astype(int)
    if target_col not in physics_df.columns:
        physics_df[target_col] = (physics_df['solexs_sdd2_ctr'] > 100.0).astype(int)
        
    def train_and_eval(df, name):
        # Drop non-numeric and target
        X = df.select_dtypes(include=[np.number]).drop(columns=[target_col, 'current_flare_peak'], errors='ignore')
        y = df[target_col]
        
        # Split
        if len(X) < 10: return None
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        model = lgb.LGBMClassifier(n_estimators=50, random_state=42, verbosity=-1)
        model.fit(X_train, y_train)
        
        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds, zero_division=0)
        brier = brier_score_loss(y_test, probs)
        
        # TSS / HSS
        cm = confusion_matrix(y_test, preds)
        if cm.shape == (2, 2):
            tn, fp, fn, tp = cm.ravel()
            tss = (tp / (tp + fn)) - (fp / (fp + tn)) if (tp+fn) > 0 and (fp+tn) > 0 else 0
            hss = 2 * (tp * tn - fp * fn) / ((tp + fn) * (fn + tn) + (tp + fp) * (fp + tn)) if ((tp + fn) * (fn + tn) + (tp + fp) * (fp + tn)) > 0 else 0
        else:
            tss, hss = 0, 0
            
        return {
            "Accuracy": acc,
            "Precision": prec,
            "Recall (TPR)": rec,
            "Brier Score": brier,
            "TSS": tss,
            "HSS": hss,
            "Feature_Importance": dict(zip(X.columns, model.feature_importances_))
        }

    res_base = train_and_eval(base_df, "Baseline")
    res_phys = train_and_eval(physics_df, "Physics-Enriched")
    
    if res_base and res_phys:
        report = f"""# Physics Validation Report
        
## Baseline Features vs Physics-Enriched Features

| Metric | Baseline | Physics-Enriched | Improvement |
|--------|----------|------------------|-------------|
| Accuracy | {res_base['Accuracy']:.4f} | {res_phys['Accuracy']:.4f} | {res_phys['Accuracy'] - res_base['Accuracy']:.4f} |
| TSS | {res_base['TSS']:.4f} | {res_phys['TSS']:.4f} | {res_phys['TSS'] - res_base['TSS']:.4f} |
| HSS | {res_base['HSS']:.4f} | {res_phys['HSS']:.4f} | {res_phys['HSS'] - res_base['HSS']:.4f} |
| Brier Score | {res_base['Brier Score']:.4f} | {res_phys['Brier Score']:.4f} | {res_base['Brier Score'] - res_phys['Brier Score']:.4f} (lower is better) |
"""
        report_path = Path(report_dir) / "Physics_Validation_Report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w") as f:
            f.write(report)
            
        logger.info(f"Physics Validation Report generated at {report_path}")
    
