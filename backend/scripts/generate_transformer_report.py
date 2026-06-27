import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))
from backend.aditya_flare.ai_engine.models.transformer import TemporalTransformerEncoder

def main():
    print("Initializing Temporal Transformer Encoder...")
    
    num_inputs = 6  # raw + physics
    d_model = 128
    nhead = 8
    num_layers = 4
    dim_feedforward = 512
    dropout = 0.2
    
    model = TemporalTransformerEncoder(num_inputs, d_model=d_model, nhead=nhead, 
                                       num_layers=num_layers, dim_feedforward=dim_feedforward, dropout=dropout)
    
    # Generate the report
    report = model.generate_report(batch_size=32, seq_len=120, num_inputs=num_inputs)
    
    final_report = "# Phase 4: Stage 4 - Transformer Report\n\n"
    final_report += report
    
    out_dir = Path("data/evaluation")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "Transformer_Report.md"
    
    with open(out_path, "w") as f:
        f.write(final_report)
        
    print(f"Report saved to {out_path}")
    print(final_report)

if __name__ == "__main__":
    main()
