import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))
from backend.aditya_flare.ai_engine.models.physics_aware_tcn import PhysicsAwareTCN

def main():
    print("Initializing Physics-Aware TCN...")
    
    num_raw_inputs = 2      # e.g., solexs_sdd2_ctr, hel1os_hxr
    num_physics_inputs = 4  # e.g., hardness_ratio, temp, em, wavelets
    num_channels = [32, 64, 128, 256] 
    kernel_size = 3
    dropout = 0.2
    
    model = PhysicsAwareTCN(num_raw_inputs, num_physics_inputs, num_channels, kernel_size=kernel_size, dropout=dropout)
    
    # Generate the report
    report = model.generate_report(batch_size=32, seq_len=120)
    
    final_report = "# Phase 4: Stage 3 - Physics-Aware TCN Report\n\n"
    final_report += report
    
    out_dir = Path("data/evaluation")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "Physics_Aware_TCN_Report.md"
    
    with open(out_path, "w") as f:
        f.write(final_report)
        
    print(f"Report saved to {out_path}")
    print(final_report)

if __name__ == "__main__":
    main()
