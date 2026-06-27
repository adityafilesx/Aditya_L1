import os
import sys
import shap
from pathlib import Path
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report

# Add the project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from backend.aditya_flare.models.dataset import load_and_prepare_dataset, get_train_test_split
from backend.aditya_flare.utils.logger import training_logger
from backend.aditya_flare.config.config_loader import config
from backend.aditya_flare.evaluation.benchmark import BenchmarkSuite
from backend.aditya_flare.evaluation.report_generator import generate_scientific_report, generate_benchmark_report
from backend.aditya_flare.evaluation.plots import plot_reliability_diagram, plot_roc_pr_curves

def train_and_evaluate():
    processed_dir = Path(config.processed_dir)
    
    training_logger.info("Initializing Nowcasting Pipeline...")
    try:
        df = load_and_prepare_dataset(processed_dir, target_threshold=config.target_threshold_cps, horizon_minutes=config.horizon_minutes)
    except Exception as e:
        training_logger.error(f"Error loading dataset: {e}")
        return

    training_logger.info("Splitting dataset into chronological train/test sets...")
    X_train, X_test, y_train, y_test = get_train_test_split(df, test_size=0.2)
    
    training_logger.info(f"Training Set: {len(X_train)} samples")
    training_logger.info(f"Testing Set: {len(X_test)} samples")
    
    training_logger.info("Training XGBoost Classifier...")
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
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        verbose=False
    )
    
    training_logger.info("Evaluating Model...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    training_logger.info(f"\\n--- Classification Report ---\\n{classification_report(y_test, y_pred)}")
    
    # Explainable AI (SHAP)
    training_logger.info("Generating SHAP Explainability (TreeExplainer)...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    # Save SHAP Summary Plot
    eval_dir = Path("data/evaluation")
    eval_dir.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, X_test, show=False)
    shap_plot_path = eval_dir / "shap_summary.png"
    plt.savefig(shap_plot_path, bbox_inches='tight')
    plt.close()
    training_logger.info(f"Saved SHAP summary plot to {shap_plot_path}")
    
    # Benchmark Framework
    training_logger.info("Running Scientific Benchmarks...")
    suite = BenchmarkSuite()
    suite.add_model("XGBoost_Nowcast", y_test, y_pred_proba)
    
    results = suite.run_benchmarks()
    
    # Generate Reports & Plots
    training_logger.info("Generating Reports and Validation Plots...")
    generate_scientific_report(results["XGBoost_Nowcast"], "data/evaluation")
    generate_benchmark_report(results, "data/evaluation")
    
    plot_reliability_diagram(y_test, y_pred_proba, eval_dir / "reliability_diagram.png")
    plot_roc_pr_curves(y_test, y_pred_proba, eval_dir / "roc_curve.png", eval_dir / "pr_curve.png")
    
    # Save the trained model to disk
    models_dir = Path(config.models_dir)
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "xgboost_nowcast.json"
    model.save_model(model_path)
    training_logger.info(f"Saved trained XGBoost model to: {model_path}")

if __name__ == "__main__":
    train_and_evaluate()
