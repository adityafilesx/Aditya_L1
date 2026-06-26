import torch
import numpy as np

def enable_dropout(model):
    """ Function to enable the dropout layers during test-time """
    for m in model.modules():
        if m.__class__.__name__.startswith('Dropout'):
            m.train()

def get_mc_predictions(model, x, num_samples=50):
    """
    Computes Monte Carlo Dropout predictions to estimate epistemic uncertainty.
    
    Args:
        model: PyTorch model
        x: Input tensor [Batch, Time, Features]
        num_samples: Number of forward passes to run with dropout enabled
        
    Returns:
        dict: Means and standard deviations for probability and flux.
    """
    model.eval()
    enable_dropout(model)
    
    prob_preds = []
    flux_preds = []
    
    with torch.no_grad():
        for _ in range(num_samples):
            # Assumes model outputs a dictionary
            out = model(x)
            prob_preds.append(out['prob'].unsqueeze(0))
            flux_preds.append(out['flux'].unsqueeze(0))
            
    prob_preds = torch.cat(prob_preds, dim=0) # [num_samples, Batch]
    flux_preds = torch.cat(flux_preds, dim=0)
    
    return {
        'prob_mean': prob_preds.mean(dim=0),
        'prob_std': prob_preds.std(dim=0),
        'flux_mean': flux_preds.mean(dim=0),
        'flux_std': flux_preds.std(dim=0)
    }

class EnsembleEstimator:
    """
    Wrapper for deep ensemble uncertainty estimation.
    """
    def __init__(self, models):
        self.models = models
        for m in self.models:
            m.eval()
            
    def predict(self, x):
        prob_preds = []
        flux_preds = []
        
        with torch.no_grad():
            for m in self.models:
                out = m(x)
                prob_preds.append(out['prob'].unsqueeze(0))
                flux_preds.append(out['flux'].unsqueeze(0))
                
        prob_preds = torch.cat(prob_preds, dim=0)
        flux_preds = torch.cat(flux_preds, dim=0)
        
        return {
            'prob_mean': prob_preds.mean(dim=0),
            'prob_std': prob_preds.std(dim=0),
            'flux_mean': flux_preds.mean(dim=0),
            'flux_std': flux_preds.std(dim=0)
        }
