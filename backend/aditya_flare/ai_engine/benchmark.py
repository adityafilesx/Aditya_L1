import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error

class BenchmarkSuite:
    """
    Compares the Temporal AI Engine against the Legacy XGBoost Engine.
    """
    def __init__(self, ai_model, xgb_model, device='cpu'):
        self.ai_model = ai_model
        if self.ai_model:
            self.ai_model.eval()
            self.ai_model.to(device)
        self.xgb_model = xgb_model
        self.device = device
        
    def evaluate_ai_model(self, test_loader):
        """
        Evaluate AI model on temporal test loader.
        """
        all_preds_prob = []
        all_preds_flux = []
        all_preds_class = []
        
        all_targets_prob = []
        all_targets_flux = []
        all_targets_class = []
        
        with torch.no_grad():
            for x, y in test_loader:
                x = x.to(self.device)
                
                sxr_dim = x.size(-1) // 3
                sxr_x = x[:, :, :sxr_dim]
                hxr_x = x[:, :, sxr_dim:2*sxr_dim]
                physics_x = x[:, :, 2*sxr_dim:]
                
                outputs = self.ai_model(sxr_x, hxr_x, physics_x)
                
                all_preds_prob.extend(outputs['prob'].cpu().numpy())
                all_preds_flux.extend(outputs['flux'].cpu().numpy())
                all_preds_class.extend(torch.argmax(outputs['class_logits'], dim=-1).cpu().numpy())
                
                all_targets_prob.extend(y[:, 0].numpy())
                all_targets_flux.extend(y[:, 1].numpy())
                all_targets_class.extend(y[:, 2].numpy())
                
        # Calculate Metrics
        prob_acc = accuracy_score(all_targets_prob, np.array(all_preds_prob) > 0.5)
        flux_mse = mean_squared_error(all_targets_flux, all_preds_flux)
        class_f1 = f1_score(all_targets_class, all_preds_class, average='weighted', zero_division=0)
        
        return {
            'Prob Accuracy': prob_acc,
            'Flux MSE': flux_mse,
            'Class F1': class_f1
        }
        
    def evaluate_xgb_model(self, X_test, y_test_prob, y_test_flux, y_test_class):
        """
        Evaluate XGBoost Baseline on tabular test set.
        Assumes xgb_model is a dictionary of models for different tasks or handles them jointly.
        """
        if not self.xgb_model:
            return {'Prob Accuracy': 0, 'Flux MSE': 0, 'Class F1': 0}
            
        # Simplified: assumes xgb_model is the prob model for demonstration
        preds_prob = self.xgb_model.predict(X_test)
        prob_acc = accuracy_score(y_test_prob, preds_prob > 0.5)
        
        return {
            'Prob Accuracy': prob_acc,
            'Flux MSE': float('nan'), # Placeholder if we don't have flux xgb
            'Class F1': float('nan')  # Placeholder
        }
        
    def compare(self, test_loader, X_test_xgb=None, y_test_xgb=None):
        ai_metrics = self.evaluate_ai_model(test_loader)
        if self.xgb_model and X_test_xgb is not None:
            # Assuming y_test_xgb is a dict of the 3 targets
            xgb_metrics = self.evaluate_xgb_model(X_test_xgb, y_test_xgb['prob'], y_test_xgb['flux'], y_test_xgb['class'])
        else:
            xgb_metrics = {'Prob Accuracy': np.nan, 'Flux MSE': np.nan, 'Class F1': np.nan}
            
        df = pd.DataFrame([ai_metrics, xgb_metrics], index=["Temporal AI", "XGBoost"])
        return df
