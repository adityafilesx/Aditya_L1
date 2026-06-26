import torch
import torch.nn as nn
import torch.nn.functional as F

class CrossAttentionFusion(nn.Module):
    """
    Implements Cross-Attention to allow the Soft X-ray (SXR) stream to attend to 
    relevant temporal features in the Hard X-ray (HXR) stream, addressing time lags.
    """
    def __init__(self, d_model=128, nhead=8, dropout=0.2):
        super(CrossAttentionFusion, self).__init__()
        self.multihead_attn = nn.MultiheadAttention(d_model, nhead, dropout=dropout, batch_first=True)
        self.layer_norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, query, key_value):
        # query is SXR, key_value is HXR
        # This allows SXR features to query the HXR context
        attn_output, attn_weights = self.multihead_attn(query, key_value, key_value)
        
        # Residual fusion
        out = self.layer_norm(query + self.dropout(attn_output))
        return out, attn_weights

class DualStreamNetwork(nn.Module):
    """
    Stage 5: Dual Stream Architecture.
    Processes SXR and HXR independently to extract distinct temporal morphology, 
    fuses them via Cross-Attention to handle asynchronous impulsivity, and then combines them.
    """
    def __init__(self, sxr_dim=1, hxr_dim=1, physics_dim=4, d_model=128, num_layers=2):
        super(DualStreamNetwork, self).__init__()
        
        # SXR Encoder (e.g., Simple LSTM or GRU for sequential encoding before attention)
        self.sxr_encoder = nn.GRU(sxr_dim, d_model, num_layers=num_layers, batch_first=True, dropout=0.2)
        
        # HXR Encoder
        self.hxr_encoder = nn.GRU(hxr_dim, d_model, num_layers=num_layers, batch_first=True, dropout=0.2)
        
        # Physics Encoder
        self.physics_encoder = nn.Linear(physics_dim, d_model)
        
        # Cross Attention Fusion
        self.sxr_cross_hxr = CrossAttentionFusion(d_model=d_model)
        
        # Late Fusion and Output
        self.fusion_fc = nn.Sequential(
            nn.Linear(d_model * 2, d_model),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        self.prob_head = nn.Linear(d_model, 1)

    def forward(self, sxr_in, hxr_in, physics_in):
        # Independent Encoding
        sxr_feat, _ = self.sxr_encoder(sxr_in)
        hxr_feat, _ = self.hxr_encoder(hxr_in)
        phys_feat = self.physics_encoder(physics_in)
        
        # Add physics features into the SXR stream before cross-attention
        sxr_feat = sxr_feat + phys_feat
        
        # Cross Attention (SXR attends to HXR)
        fused_sxr, attn_weights = self.sxr_cross_hxr(query=sxr_feat, key_value=hxr_feat)
        
        # Take the last hidden states for late fusion
        last_sxr = fused_sxr[:, -1, :]
        last_hxr = hxr_feat[:, -1, :]
        
        # Late Fusion
        concat = torch.cat([last_sxr, last_hxr], dim=-1)
        final_rep = self.fusion_fc(concat)
        
        # Prediction
        prob = torch.sigmoid(self.prob_head(final_rep))
        
        return prob, attn_weights
        
    def generate_report(self, batch_size=32, seq_len=120, sxr_dim=1, hxr_dim=1, physics_dim=4):
        import time
        
        params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        # Benchmark Latency
        self.eval()
        d_sxr = torch.randn(batch_size, seq_len, sxr_dim)
        d_hxr = torch.randn(batch_size, seq_len, hxr_dim)
        d_phys = torch.randn(batch_size, seq_len, physics_dim)
        
        # Warmup
        with torch.no_grad():
            for _ in range(10):
                _ = self(d_sxr, d_hxr, d_phys)
                
        # Time
        start = time.perf_counter()
        with torch.no_grad():
            for _ in range(100):
                _ = self(d_sxr, d_hxr, d_phys)
        end = time.perf_counter()
        
        avg_latency_ms = ((end - start) / 100) * 1000
        
        report = f"### Stage 5: Dual Stream Architecture Report\n"
        report += f"- **Parameters**: {params:,}\n"
        report += f"- **Latency (BS={batch_size}, L={seq_len})**: {avg_latency_ms:.2f} ms\n"
        report += f"- **Memory Estimate**: ~{params * 4 / (1024**2):.2f} MB (Weights only)\n"
        report += f"- **Added Mechanism**: Independent SXR/HXR Encoders + Cross-Attention\n"
        
        return report

