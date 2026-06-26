import torch
import torch.nn as nn
from .tcn import TemporalConvNet
from .transformer import TemporalTransformerEncoder
from .physics_aware_tcn import PhysicsAwareTCN

class TemporalFlareModel(nn.Module):
    """
    Complete Temporal AI Engine model architecture integrating:
    - SXR and HXR Temporal Convolutional Networks
    - Temporal Transformer Encoder
    - Cross-attention Dual Stream Fusion
    - Physics Attention Mechanism
    - Multi-Task Head
    """
    def __init__(self, 
                 sxr_dim, 
                 hxr_dim, 
                 physics_dim,
                 tcn_channels=[64, 128, 256], 
                 kernel_size=2, 
                 d_model=256, 
                 nhead=4, 
                 num_layers=2, 
                 num_classes=5,
                 dropout=0.2):
        super(TemporalFlareModel, self).__init__()
        
        # Stream Encoders (TCN)
        self.sxr_tcn = TemporalConvNet(num_inputs=sxr_dim, num_channels=tcn_channels, kernel_size=kernel_size, dropout=dropout)
        self.hxr_tcn = TemporalConvNet(num_inputs=hxr_dim, num_channels=tcn_channels, kernel_size=kernel_size, dropout=dropout)
        
        # Dual Stream Fusion via Cross Attention
        self.fusion = DualStreamFusion(sxr_dim=tcn_channels[-1], hxr_dim=tcn_channels[-1], num_heads=nhead, dropout=dropout)
        fused_dim = tcn_channels[-1] * 2
        
        # Physics Attention integration
        self.physics_attention = PhysicsAttention(feature_dim=physics_dim, hidden_dim=64)
        
        # Final combined dimension before transformer
        combined_dim = fused_dim + physics_dim
        
        # Temporal Transformer
        self.transformer = TemporalTransformer(
            num_inputs=combined_dim, d_model=d_model, nhead=nhead, 
            num_layers=num_layers, dim_feedforward=512, dropout=dropout
        )
        
        # Multi-task Head
        self.head = MultiTaskHead(hidden_dim=d_model, num_classes=num_classes)

    def forward(self, sxr_x, hxr_x, physics_x):
        """
        sxr_x: [Batch, Time, SxrDim]
        hxr_x: [Batch, Time, HxrDim]
        physics_x: [Batch, Time, PhysicsDim]
        """
        # Temporal encoding
        sxr_feat = self.sxr_tcn(sxr_x)
        hxr_feat = self.hxr_tcn(hxr_x)
        
        # Cross-attention fusion
        fused_feat, _, _ = self.fusion(sxr_feat, hxr_feat)
        
        # Physics attention
        phys_feat, _ = self.physics_attention(physics_x)
        
        # Concatenate features
        combined_feat = torch.cat([fused_feat, phys_feat], dim=-1)
        
        # Global temporal context via Transformer
        trans_feat = self.transformer(combined_feat)
        
        # We take the representation from the last timestep for prediction
        last_step_feat = trans_feat[:, -1, :]
        
        # Multi-task prediction
        outputs = self.head(last_step_feat)
        return outputs
