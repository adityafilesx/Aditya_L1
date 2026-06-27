import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))
from backend.aditya_flare.ai_engine.models.tcn import TemporalConvNet

def main():
    print("Initializing Temporal Convolutional Network (TCN) Baseline...")
    
    # 4 input features: solexs_sdd2_ctr, hardness_ratio, goes_xrsa_flux, goes_xrsb_flux
    num_inputs = 4
    num_channels = [32, 64, 128, 256] 
    kernel_size = 3
    dropout = 0.2
    
    tcn_model = TemporalConvNet(num_inputs, num_channels, kernel_size=kernel_size, dropout=dropout)
    
    # Generate the report
    report = tcn_model.generate_report(batch_size=32, seq_len=120, num_inputs=num_inputs)
    
    final_report = "# Phase 4: Stage 2 - TCN Baseline Report\n\n"
    final_report += report
    
    out_dir = Path("data/evaluation")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "TCN_Baseline_Report.md"
    
    with open(out_path, "w") as f:
        f.write(final_report)
        
    print(f"Report saved to {out_path}")
    print(final_report)

if __name__ == "__main__":
    main()
