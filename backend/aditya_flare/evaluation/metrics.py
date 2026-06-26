import numpy as np
from sklearn.metrics import confusion_matrix, brier_score_loss, roc_auc_score, average_precision_score

def compute_skill_scores(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    tss = tpr - fpr
    
    numerator = 2 * (tp * tn - fp * fn)
    denominator = (tp + fn) * (fn + tn) + (tp + fp) * (fp + tn)
    hss = numerator / denominator if denominator > 0 else 0
    
    far = fp / (fp + tp) if (fp + tp) > 0 else 0
    
    return {
        'TSS': tss,
        'HSS': hss,
        'TPR': tpr,
        'FPR': fpr,
        'FAR': far,
        'TP': tp,
        'FP': fp,
        'FN': fn,
        'TN': tn
    }

def compute_calibration_errors(y_true, y_prob, n_bins=10):
    """
    Computes Expected Calibration Error (ECE) and Maximum Calibration Error (MCE).
    """
    bins = np.linspace(0., 1., n_bins + 1)
    binids = np.digitize(y_prob, bins) - 1
    
    bin_sums = np.bincount(binids, weights=y_prob, minlength=len(bins))
    bin_true = np.bincount(binids, weights=y_true, minlength=len(bins))
    bin_total = np.bincount(binids, minlength=len(bins))
    
    nonzero = bin_total != 0
    prob_true = bin_true[nonzero] / bin_total[nonzero]
    prob_pred = bin_sums[nonzero] / bin_total[nonzero]
    
    ece = np.sum(np.abs(prob_true - prob_pred) * (bin_total[nonzero] / len(y_true)))
    mce = np.max(np.abs(prob_true - prob_pred))
    
    return ece, mce

def compute_all_metrics(y_true, y_prob, threshold=0.5):
    y_pred = (np.array(y_prob) >= threshold).astype(int)
    scores = compute_skill_scores(y_true, y_pred)
    
    ece, mce = compute_calibration_errors(y_true, y_prob)
    brier = brier_score_loss(y_true, y_prob)
    try:
        roc_auc = roc_auc_score(y_true, y_prob)
    except ValueError:
        roc_auc = 0.0
    pr_auc = average_precision_score(y_true, y_prob)
    
    scores.update({
        'ECE': ece,
        'MCE': mce,
        'Brier': brier,
        'ROC_AUC': roc_auc,
        'PR_AUC': pr_auc
    })
    
    return scores
