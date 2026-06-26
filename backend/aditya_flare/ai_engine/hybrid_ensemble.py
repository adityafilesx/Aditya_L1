import numpy as np

class HybridEnsemble:
    """
    Combines predictions from the legacy XGBoost engine and the new Temporal AI Engine.
    """
    def __init__(self, ai_weight=0.5, xgb_weight=0.5, dynamic_weighting=False):
        self.ai_weight = ai_weight
        self.xgb_weight = xgb_weight
        self.dynamic_weighting = dynamic_weighting

    def predict(self, ai_preds, xgb_preds, ai_uncertainty=None, xgb_uncertainty=None):
        """
        ai_preds: dict {'prob', 'flux', 'class'}
        xgb_preds: dict {'prob', 'flux', 'class'}
        """
        
        if self.dynamic_weighting and ai_uncertainty is not None:
            # Simple heuristic: inversely proportional to uncertainty
            # Assuming uncertainty is standard deviation
            ai_w = 1.0 / (ai_uncertainty + 1e-5)
            xgb_w = 1.0 / (xgb_uncertainty + 1e-5) if xgb_uncertainty else 1.0
            
            total_w = ai_w + xgb_w
            w_ai = ai_w / total_w
            w_xgb = xgb_w / total_w
        else:
            w_ai = self.ai_weight
            w_xgb = self.xgb_weight
            
        final_prob = w_ai * ai_preds['prob'] + w_xgb * xgb_preds['prob']
        
        # XGBoost might not have flux predictions, handle conditionally
        if 'flux' in xgb_preds and xgb_preds['flux'] is not None and not np.isnan(xgb_preds['flux']):
            final_flux = w_ai * ai_preds['flux'] + w_xgb * xgb_preds['flux']
        else:
            final_flux = ai_preds['flux']
            
        # Class: defer to AI for full classes
        final_class = ai_preds['class']
        
        return {
            'prob': final_prob,
            'flux': final_flux,
            'class': final_class,
            'weights_used': {'ai': w_ai, 'xgb': w_xgb}
        }
