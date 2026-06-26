import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    """
    Standard trigonometric positional encoding to inject temporal order.
    """
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        if d_model % 2 != 0:
            pe[:, 1::2] = torch.cos(position * div_term[:-1])
        else:
            pe[:, 1::2] = torch.cos(position * div_term)
            
        pe = pe.unsqueeze(0)  # Shape: [1, max_len, d_model]
        self.register_buffer('pe', pe)

    def forward(self, x):
        """
        x shape: [batch_size, seq_len, d_model]
        """
        x = x + self.pe[:, :x.size(1), :]
        return x

class TemporalTransformerEncoder(nn.Module):
    """
    Stage 4: Encoder-only Temporal Transformer.
    Implements causal masking to prevent future data leakage.
    """
    def __init__(self, num_inputs, d_model=128, nhead=8, num_layers=4, dim_feedforward=512, dropout=0.2):
        super(TemporalTransformerEncoder, self).__init__()
        
        self.d_model = d_model
        
        # Input projection
        self.input_proj = nn.Linear(num_inputs, d_model)
        
        # Positional Encoding
        self.pos_encoder = PositionalEncoding(d_model)
        
        # Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, 
            nhead=nhead, 
            dim_feedforward=dim_feedforward, 
            dropout=dropout, 
            activation='gelu',
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Output Head
        self.prob_head = nn.Linear(d_model, 1)
        
    def generate_square_subsequent_mask(self, sz):
        """
        Generates a causal mask to ensure the model cannot look ahead in time.
        """
        mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
        mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
        return mask

    def forward(self, x):
        # x is expected to be [Batch, Time, Features]
        seq_len = x.size(1)
        
        # Project inputs to d_model
        x = self.input_proj(x)
        
        # Add positional encoding
        x = self.pos_encoder(x)
        
        # Generate causal mask
        causal_mask = self.generate_square_subsequent_mask(seq_len).to(x.device)
        
        # Pass through Transformer
        out = self.transformer_encoder(x, mask=causal_mask, is_causal=True)
        
        # Take the last time step for prediction
        last_step = out[:, -1, :]
        prob = torch.sigmoid(self.prob_head(last_step))
        return prob
        
    def generate_report(self, batch_size=32, seq_len=120, num_inputs=6):
        import time
        
        params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        
        # Benchmark Latency
        self.eval()
        dummy_input = torch.randn(batch_size, seq_len, num_inputs)
        
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
        
        report = f"### Stage 4: Transformer Architecture Report\n"
        report += f"- **Parameters**: {params:,}\n"
        report += f"- **Latency (BS={batch_size}, L={seq_len})**: {avg_latency_ms:.2f} ms\n"
        report += f"- **Memory Estimate**: ~{params * 4 / (1024**2):.2f} MB (Weights only)\n"
        report += f"- **Added Mechanism**: Self-Attention & Causal Masking\n"
        
        return report
