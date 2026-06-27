import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))
from backend.aditya_flare.ai_engine.models.dual_stream import DualStreamNetwork

def main():
    print("Initializing Dual Stream Architecture...")
    
    # 1 dim for SXR, 1 for HXR, 4 for Physics
    model = DualStreamNetwork(sxr_dim=1, hxr_dim=1, physics_dim=4, d_model=128, num_layers=2)
    
    # Generate the report
    report = model.generate_report(batch_size=32, seq_len=120, sxr_dim=1, hxr_dim=1, physics_dim=4)
    
    final_report = "# Phase 4: Stage 5 - Dual Stream Architecture Report\n\n"
    final_report += report
    
    out_dir = Path("data/evaluation")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "Dual_Stream_Report.md"
    
    with open(out_path, "w") as f:
        f.write(final_report)
        
    print(f"Report saved to {out_path}")
    print(final_report)

if __name__ == "__main__":
    main()
