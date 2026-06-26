import torch
import torch.nn as nn
from .tcn import TemporalConvNet

class PhysicsFeatureGating(nn.Module):
    """
    Adaptive gating mechanism to learn how much to trust physical features dynamically.
    Instead of hard-coding feature importance, this network computes a temporal mask 
    based on the raw telemetry to selectively let physics features influence the embedding.
    """
    def __init__(self, raw_dim, physics_dim, hidden_dim=64):
        super(PhysicsFeatureGating, self).__init__()
        self.context_net = nn.Sequential(
            nn.Linear(raw_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, physics_dim),
            nn.Sigmoid()  # Gates between 0 and 1
        )
        
        self.physics_proj = nn.Linear(physics_dim, physics_dim)
        
    def forward(self, raw_features, physics_features):
        # Compute confidence/gate purely from raw signal context
        gate = self.context_net(raw_features)
        
        # Project and gate physics features
        gated_physics = self.physics_proj(physics_features) * gate
        return gated_physics, gate

class PhysicsAwareTCN(nn.Module):
    """
    Stage 3: Physics-Aware TCN.
    Injects physics features into the sequence processing pipeline via an adaptive gating layer.
    """
    def __init__(self, num_raw_inputs, num_physics_inputs, num_channels, kernel_size=3, dropout=0.2):
        super(PhysicsAwareTCN, self).__init__()
        
        self.num_raw_inputs = num_raw_inputs
        self.num_physics_inputs = num_physics_inputs
        
        # Gating mechanism
        self.physics_gating = PhysicsFeatureGating(num_raw_inputs, num_physics_inputs)
        
        # Base TCN takes both raw and gated physics features
        total_inputs = num_raw_inputs + num_physics_inputs
        self.tcn = TemporalConvNet(total_inputs, num_channels, kernel_size=kernel_size, dropout=dropout)
        
    def forward(self, x):
        # x is expected to be [Batch, Time, Features]
        # Split features into raw telemetry and physics
        raw_features = x[:, :, :self.num_raw_inputs]
        physics_features = x[:, :, self.num_raw_inputs:]
        
        # Apply physics gating
        gated_physics, gate_weights = self.physics_gating(raw_features, physics_features)
        
        # Concatenate raw and gated physics for the temporal convolution
        fused_input = torch.cat([raw_features, gated_physics], dim=-1)
        
        # Pass to TCN
        prob = self.tcn(fused_input)
        
        return prob, gate_weights
        
    def generate_report(self, batch_size=32, seq_len=120):
        import time
        
        params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        # Benchmark Latency
        self.eval()
        dummy_input = torch.randn(batch_size, seq_len, self.num_raw_inputs + self.num_physics_inputs)
        
        # Warmup
        with torch.no_grad():
            for _ in range(10):
                _ = self(dummy_input)
                
        # Time
        start = time.perf_counter()
        with torch.no_grad():
            for _ in range(100):
                _ = self(dummy_input)
        end = time.perf_counter()
        
        avg_latency_ms = ((end - start) / 100) * 1000
        
        report = f"### Stage 3: Physics-Aware TCN Architecture Report\n"
        report += f"- **Parameters**: {params:,}\n"
        report += f"- **Latency (BS={batch_size}, L={seq_len})**: {avg_latency_ms:.2f} ms\n"
        report += f"- **Memory Estimate**: ~{params * 4 / (1024**2):.2f} MB (Weights only)\n"
        report += f"- **Added Mechanism**: Adaptive Physics Feature Gating\n"
        
        return report

