import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve
from sklearn.metrics import roc_curve, precision_recall_curve

def plot_reliability_diagram(y_true, y_prob, output_path: str):
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10)
    
    plt.figure(figsize=(8, 8))
    plt.plot([0, 1], [0, 1], linestyle='--', label='Perfectly calibrated', color='black')
    plt.plot(prob_pred, prob_true, marker='o', label='Model', color='blue')
    
    plt.xlabel('Mean Predicted Probability')
    plt.ylabel('Fraction of Positives')
    plt.title('Reliability Diagram (Calibration Curve)')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_roc_pr_curves(y_true, y_prob, roc_path: str, pr_path: str):
    try:
        # ROC
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.grid(True, alpha=0.3)
        plt.savefig(roc_path)
        plt.close()
    except Exception:
        pass
        
    try:
        # PR
        prec, rec, _ = precision_recall_curve(y_true, y_prob)
        plt.figure(figsize=(8, 6))
        plt.plot(rec, prec, color='green', lw=2)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.grid(True, alpha=0.3)
        plt.savefig(pr_path)
        plt.close()
    except Exception:
        pass
