import os
import sys
from pathlib import Path
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, precision_recall_curve

# Add the project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from aditya_flare.models.dataset import load_and_prepare_dataset, get_train_test_split

def train_and_evaluate():
    processed_dir = Path("data/processed")
    
    print("Initializing Nowcasting Pipeline...")
    # Load and prepare features & target
    # We set target_threshold=500 (counts/sec) and horizon_minutes=15
    try:
        df = load_and_prepare_dataset(processed_dir, target_threshold=500, horizon_minutes=15)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    print("Splitting dataset into chronological train/test sets...")
    X_train, X_test, y_train, y_test = get_train_test_split(df, test_size=0.2)
    
    print(f"Training Set: {len(X_train)} samples")
    print(f"Testing Set: {len(X_test)} samples")
    
    print("Training XGBoost Classifier...")
    # Use GPU hist method if available, otherwise hist
    model = xgb.XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric='auc',
        early_stopping_rounds=20,
        random_state=42
    )
    
    # We use a validation set for early stopping
    model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        verbose=10
    )
    
    print("\\nEvaluating Model...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    print("\\n--- Classification Report ---")
    print(classification_report(y_test, y_pred))
    
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"ROC-AUC Score: {auc:.4f}")
    
    # --- Generate Plots ---
    print("\\nGenerating Evaluation Plots...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Feature Importance
    importance = model.feature_importances_
    features = X_train.columns
    sns.barplot(x=importance, y=features, ax=ax1, palette='viridis')
    ax1.set_title("XGBoost Feature Importance")
    ax1.set_xlabel("F-Score")
    
    # Plot 2: ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    ax2.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {auc:.2f})')
    ax2.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    ax2.set_xlim([0.0, 1.0])
    ax2.set_ylim([0.0, 1.05])
    ax2.set_xlabel('False Positive Rate')
    ax2.set_ylabel('True Positive Rate')
    ax2.set_title('Receiver Operating Characteristic')
    ax2.legend(loc="lower right")
    
    plt.tight_layout()
    
    # Save the plot directly into the artifacts directory so the user can easily view it
    artifact_dir = "/Users/aditya1981/.gemini/antigravity-ide/brain/db247a25-938f-4041-9c38-4920d6c3682f"
    plot_path = os.path.join(artifact_dir, "xgboost_evaluation.png")
    plt.savefig(plot_path)
    print(f"Saved evaluation plots to: {plot_path}")
    
    # Save the trained model to disk
    models_dir = Path("data/models")
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "xgboost_nowcast.json"
    model.save_model(model_path)
    print(f"\\nSaved trained XGBoost model to: {model_path}")

if __name__ == "__main__":
    train_and_evaluate()
