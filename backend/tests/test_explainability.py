import pytest
import xgboost as xgb
import numpy as np
import shap

def test_shap_explainer():
    X = np.random.rand(100, 5)
    y = np.random.randint(2, size=100)
    
    model = xgb.XGBClassifier(n_estimators=10)
    model.fit(X, y)
    
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X[:10])
    
    assert shap_values is not None
    assert shap_values.shape == (10, 5)
