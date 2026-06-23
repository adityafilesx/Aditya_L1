import os
import sys
import pickle
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE
import lightgbm as lgb
import mlflow

# Ensure path resolution
sys.path.append(str(Path(__file__).parent.parent.parent))
from aditya_flare.processing.features import extract_features

def compute_skill_scores(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    tss = tpr - fpr
    
    numerator = 2 * (tp * tn - fp * fn)
    denominator = (tp + fn) * (fn + tn) + (tp + fp) * (fp + tn)
    hss = numerator / denominator if denominator > 0 else 0
    
    return tss, hss, tp, fp, fn, tn

def train_ensemble_forecaster(processed_dir: str, horizon_minutes: int = 15, threshold: float = 500.0):
    print("Extracting features (This may take a moment)...")
    df = extract_features(processed_dir, flare_threshold=threshold)
    
    print(f"Labeling target variable (Horizon: {horizon_minutes}m)...")
    # Y_t: Flare in forward window (t+1, t+N]
    future_max = df['solexs_sdd2_ctr'].shift(-1)[::-1].rolling(horizon_minutes, min_periods=1).max()[::-1]
    df['target'] = (future_max >= threshold).astype(int)
    
    # Exclude data points that fall *inside* an active flare
    # We only want to forecast the onset from a quiet or pre-flare state.
    df = df[df['is_flare'] == 0].copy()
    
    # Drop rows that have NaNs due to shifting
    df = df.dropna()
    
    # Define features
    exclude_cols = ['target', 'is_flare']
    features = [c for c in df.columns if c not in exclude_cols]
    
    X = df[features].values
    y = df['target'].values
    
    print(f"Data ready. Total samples (quiet-sun onset prediction): {len(X)}")
    print(f"Target distribution: {np.bincount(y)}")
    
    tscv = TimeSeriesSplit(n_splits=3)
    
    tss_scores = []
    hss_scores = []
    
    fold = 1
    for train_index, test_index in tscv.split(X):
        print(f"\\n--- Fold {fold} ---")
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        # 1. Apply SMOTE ONLY on the training fold
        print("Applying SMOTE to training fold...")
        smote = SMOTE(random_state=42)
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
        
        # 2. Train Model A: LightGBM
        print("Training LightGBM...")
        lgb_model = lgb.LGBMClassifier(
            class_weight='balanced',
            n_estimators=150,
            learning_rate=0.05,
            random_state=42,
            verbose=-1
        )
        lgb_model.fit(X_train_res, y_train_res)
        
        # 3. Train Model B: kNN (L1 distance, k=1)
        print("Training k-NN...")
        knn_model = KNeighborsClassifier(n_neighbors=1, p=1)
        knn_model.fit(X_train_res, y_train_res)
        
        # 4. Ensemble Soft Voting (0.7 LGB, 0.3 kNN)
        print("Evaluating Ensemble...")
        p_lgb = lgb_model.predict_proba(X_test)[:, 1]
        p_knn = knn_model.predict_proba(X_test)[:, 1]
        
        p_ensemble = (0.7 * p_lgb) + (0.3 * p_knn)
        y_pred = (p_ensemble >= 0.5).astype(int)
        
        tss, hss, tp, fp, fn, tn = compute_skill_scores(y_test, y_pred)
        
        print(f"Confusion Matrix: TP={tp}, FP={fp}, FN={fn}, TN={tn}")
        print(f"True Skill Statistic (TSS): {tss:.4f}")
        print(f"Heidke Skill Score (HSS):   {hss:.4f}")
        
        tss_scores.append(tss)
        hss_scores.append(hss)
        fold += 1
        
    print("\\n==================================")
    print(f"Average CV TSS: {np.mean(tss_scores):.4f}")
    print(f"Average CV HSS: {np.mean(hss_scores):.4f}")
    
    # Finally, retrain on FULL dataset to save the final models
    print("\\nRetraining final ensemble on entire dataset...")
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X, y)
    
    final_lgb = lgb.LGBMClassifier(class_weight='balanced', n_estimators=150, learning_rate=0.05, random_state=42, verbose=-1)
    final_lgb.fit(X_res, y_res)
    
    final_knn = KNeighborsClassifier(n_neighbors=1, p=1)
    final_knn.fit(X_res, y_res)
    
    # Save artifacts
    models_dir = Path("data/models")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    with open(models_dir / "ensemble_forecaster.pkl", "wb") as f:
        pickle.dump({
            'lgb': final_lgb,
            'knn': final_knn,
            'features': features,
            'weights': {'lgb': 0.7, 'knn': 0.3}
        }, f)
        
    print("Successfully saved ensemble model to data/models/ensemble_forecaster.pkl")

if __name__ == "__main__":
    train_ensemble_forecaster("data/processed")
