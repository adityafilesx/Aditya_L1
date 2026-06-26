import torch
import torch.nn as nn
import torch.nn.functional as F

class PhysicsAttention(nn.Module):
    """
    Computes attention weights over the input features based on physics priors.
    Specifically designed to highlight thermodynamic and spectral features during active periods.
    """
    def __init__(self, feature_dim, hidden_dim=64):
        super(PhysicsAttention, self).__init__()
        self.attention_net = nn.Sequential(
            nn.Linear(feature_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, feature_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        """
        x: [Batch, Time, FeatureDim]
        Returns: Attention-weighted features of the same shape.
        """
        # attention_weights: [Batch, Time, FeatureDim]
        attention_weights = self.attention_net(x)
        
        # Apply weights to features
        weighted_features = x * attention_weights
        
        return weighted_features, attention_weights
