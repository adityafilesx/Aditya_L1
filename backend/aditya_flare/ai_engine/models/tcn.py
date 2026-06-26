import torch
import torch.nn as nn
from torch.nn.utils import weight_norm

class Chomp1d(nn.Module):
    """
    Removes the padding on the right side of the sequence to ensure causal convolutions.
    """
    def __init__(self, chomp_size):
        super(Chomp1d, self).__init__()
        self.chomp_size = chomp_size

    def forward(self, x):
        return x[:, :, :-self.chomp_size].contiguous()

class TemporalBlock(nn.Module):
    """
    A single Residual Block for the Temporal Convolutional Network.
    Includes causal dilated convolutions, weight normalization, ReLU, and dropout.
    """
    def __init__(self, n_inputs, n_outputs, kernel_size, stride, dilation, padding, dropout=0.2):
        super(TemporalBlock, self).__init__()
        
        # Conv 1
        self.conv1 = weight_norm(nn.Conv1d(n_inputs, n_outputs, kernel_size,
                                           stride=stride, padding=padding, dilation=dilation))
        self.chomp1 = Chomp1d(padding)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(dropout)

        # Conv 2
        self.conv2 = weight_norm(nn.Conv1d(n_outputs, n_outputs, kernel_size,
                                           stride=stride, padding=padding, dilation=dilation))
        self.chomp2 = Chomp1d(padding)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(dropout)

        self.net = nn.Sequential(self.conv1, self.chomp1, self.relu1, self.dropout1,
                                 self.conv2, self.chomp2, self.relu2, self.dropout2)
                                 
        self.downsample = nn.Conv1d(n_inputs, n_outputs, 1) if n_inputs != n_outputs else None
        self.relu = nn.ReLU()
        self.init_weights()

    def init_weights(self):
        self.conv1.weight.data.normal_(0, 0.01)
        self.conv2.weight.data.normal_(0, 0.01)
        if self.downsample is not None:
            self.downsample.weight.data.normal_(0, 0.01)

    def forward(self, x):
        out = self.net(x)
        res = x if self.downsample is None else self.downsample(x)
        return self.relu(out + res)


class TemporalConvNet(nn.Module):
    """
    Temporal Convolutional Network (TCN) Baseline.
    Implements a hierarchy of TemporalBlocks to establish an adaptive receptive field.
    """
    def __init__(self, num_inputs, num_channels, kernel_size=2, dropout=0.2):
        """
        num_inputs: Number of input features
        num_channels: List of channel sizes for each hidden layer
        kernel_size: Size of the convolutional kernel
        dropout: Dropout rate
        """
        super(TemporalConvNet, self).__init__()
        layers = []
        num_levels = len(num_channels)
        self.receptive_field = 1
        
        for i in range(num_levels):
            dilation_size = 2 ** i
            in_channels = num_inputs if i == 0 else num_channels[i-1]
            out_channels = num_channels[i]
            
            # Padding is calculated to ensure causal property (stride=1)
            padding = (kernel_size - 1) * dilation_size
            
            layers.append(TemporalBlock(in_channels, out_channels, kernel_size, stride=1, 
                                        dilation=dilation_size, padding=padding, dropout=dropout))
            
            self.receptive_field += 2 * (kernel_size - 1) * dilation_size

        self.network = nn.Sequential(*layers)
        
        # Classification/Regression Heads
        self.flatten = nn.Flatten()
        
        # For evaluation, we will output embeddings. The multi-task layer comes later in Stage 6.
        # But to be trainable alone as a baseline, we'll add a simple head.
        self.prob_head = nn.Linear(num_channels[-1], 1)
        
    def forward(self, x):
        # x is expected to be [Batch, Time, Features]
        # Conv1D expects [Batch, Channels (Features), Time]
        x = x.transpose(1, 2)
        out = self.network(x)
        
        # Take the last time step for prediction
        last_step = out[:, :, -1]
        
        prob = torch.sigmoid(self.prob_head(last_step))
        return prob
        
    def generate_report(self, batch_size=32, seq_len=120, num_inputs=4):
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
        
        report = f"### Stage 2: TCN Baseline Architecture Report\n"
        report += f"- **Parameters**: {params:,}\n"
        report += f"- **Receptive Field**: {self.receptive_field} time steps\n"
        report += f"- **Latency (BS={batch_size}, L={seq_len})**: {avg_latency_ms:.2f} ms\n"
        report += f"- **Memory Estimate**: ~{params * 4 / (1024**2):.2f} MB (Weights only)\n"
        
        return report

