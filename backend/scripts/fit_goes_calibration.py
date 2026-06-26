import os
import yaml
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import linregress
import matplotlib.pyplot as plt

def main():
    print("="*60)
    print("    Aditya-L1 SoLEXS to GOES Cross-Calibration Ingester")
    print("="*60)
    
    processed_dir = Path("data/processed")
    aligned_file = processed_dir / "aligned_goes_solexs.parquet"
    
    if not aligned_file.exists():
        print(f"Error: Aligned dataset {aligned_file} not found. Please run scripts/align_datasets.py first.")
        return
        
    # Load dataset
    df = pd.read_parquet(aligned_file)
    print(f"Loaded {len(df)} aligned records from {aligned_file.name}")
    
    # Filter valid non-zero values for log scale
    df_valid = df[(df['solexs_sdd2_ctr'] > 0) & (df['goes_xrsb_flux'] > 0)].copy()
    print(f"Filtered to {len(df_valid)} valid non-zero records for log-log regression.")
    
    # Extract log10 values
    X = np.log10(df_valid['solexs_sdd2_ctr'].values)
    y = np.log10(df_valid['goes_xrsb_flux'].values)
    
    # 1. Fit Log-Log Linear Regression
    # y = slope * X + intercept
    slope, intercept, r_value, p_value, std_err = linregress(X, y)
    r2_score = r_value ** 2
    
    print("\nFitted Log-Log Regression Model:")
    print(f"  log10(Flux_GOES) = {slope:.5f} * log10(cps_SoLEXS) + ({intercept:.5f})")
    print(f"  R^2 Fit Score:      {r2_score:.5f}")
    print(f"  Correlation (r):    {r_value:.5f}")
    print(f"  Standard Error:     {std_err:.5f}")
    
    # 2. Evaluate Baseline Empirical Model
    # Baseline: slope=1.05, intercept=-9.5
    baseline_slope = 1.05
    baseline_intercept = -9.5
    
    # Compute Log-space Predictions
    y_pred_fitted = slope * X + intercept
    y_pred_baseline = baseline_slope * X + baseline_intercept
    
    rmse_fitted = np.sqrt(np.mean((y - y_pred_fitted) ** 2))
    rmse_baseline = np.sqrt(np.mean((y - y_pred_baseline) ** 2))
    
    print("\nModel Evaluation (in Log10 Space):")
    print(f"  Baseline Empirical Model RMSE:   {rmse_baseline:.5f}")
    print(f"  Fitted Data-Driven Model RMSE:   {rmse_fitted:.5f}")
    print(f"  Error Reduction Percentage:      {((rmse_baseline - rmse_fitted) / rmse_baseline) * 100:.1f}%")
    
    # 3. Fit 2nd Degree Polynomial Model (Non-linear effects)
    poly_coefs = np.polyfit(X, y, 2)
    y_pred_poly = np.polyval(poly_coefs, X)
    rmse_poly = np.sqrt(np.mean((y - y_pred_poly) ** 2))
    print(f"\nFitted 2nd Degree Polynomial Model:")
    print(f"  log10(Flux_GOES) = {poly_coefs[0]:.5f} * X^2 + {poly_coefs[1]:.5f} * X + ({poly_coefs[2]:.5f})")
    print(f"  Polynomial Model RMSE:           {rmse_poly:.5f}")
    
    # 4. Save Calibration Coefficients to YAML Configuration
    cal_config_path = Path("aditya_flare/calibration/calibration_config.yaml")
    print(f"\nUpdating configuration file: {cal_config_path.resolve()}")
    
    config_data = {
        "bounds": {
            "lower": float(10 ** X.min()),
            "upper": float(10 ** X.max())
        },
        "scale": {
            "slope": float(slope),
            "intercept": float(intercept)
        },
        "polynomial": {
            "a": float(poly_coefs[0]),
            "b": float(poly_coefs[1]),
            "c": float(poly_coefs[2])
        }
    }
    
    with open(cal_config_path, "w") as f:
        yaml.safe_dump(config_data, f, default_flow_style=False)
    print("Configuration updated successfully!")
    
    # 5. Generate Calibration Plot
    docs_dir = Path("docs")
    docs_dir.mkdir(parents=True, exist_ok=True)
    plot_file = docs_dir / "goes_solexs_calibration.png"
    
    print(f"\nGenerating calibration plot: {plot_file.resolve()}")
    plt.figure(figsize=(10, 7), dpi=300)
    
    # Plot sample data points (density scatter)
    # Using small alpha and dot size to represent dense data
    plt.scatter(df_valid['solexs_sdd2_ctr'], df_valid['goes_xrsb_flux'], 
                color='#1f77b4', alpha=0.15, s=2, label="Aligned Observations (1-min cadence)")
    
    # Generate line values
    x_line = np.linspace(df_valid['solexs_sdd2_ctr'].min(), df_valid['solexs_sdd2_ctr'].max(), 500)
    x_line_log = np.log10(x_line)
    
    y_fitted = 10 ** (slope * x_line_log + intercept)
    y_baseline = 10 ** (baseline_slope * x_line_log + baseline_intercept)
    y_poly = 10 ** np.polyval(poly_coefs, x_line_log)
    
    plt.plot(x_line, y_baseline, color='#d62728', linestyle='--', linewidth=1.5,
             label=f"Baseline empirical: log(Flux) = 1.05 * log(cps) - 9.5 (RMSE={rmse_baseline:.3f})")
             
    plt.plot(x_line, y_fitted, color='#2ca02c', linestyle='-', linewidth=2,
             label=f"Fitted Data-driven Linear: log(Flux) = {slope:.3f} * log(cps) + {intercept:.2f} (R²={r2_score:.4f}, RMSE={rmse_fitted:.3f})")
             
    plt.plot(x_line, y_poly, color='#ff7f0e', linestyle='-.', linewidth=2,
             label=f"Fitted Polynomial: y = {poly_coefs[0]:.2f}X² + {poly_coefs[1]:.2f}X + {poly_coefs[2]:.2f} (RMSE={rmse_poly:.3f})")
             
    # Annotate GOES classes in plot
    classes = [
        ("A-Class", 1e-8, '#bcbd22'),
        ("B-Class", 1e-7, '#17becf'),
        ("C-Class", 1e-6, '#9467bd'),
        ("M-Class", 1e-5, '#e377c2'),
        ("X-Class", 1e-4, '#8c564b')
    ]
    for name, level, color in classes:
        plt.axhline(level, color=color, alpha=0.2, linestyle=':')
        plt.text(df_valid['solexs_sdd2_ctr'].max() * 0.4, level * 1.2, name, color=color, fontsize=9, alpha=0.7)
        
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Aditya-L1 SoLEXS SDD2 Count Rate (cps)", fontsize=11, fontweight='bold')
    plt.ylabel("NOES GOES XRSB Soft X-Ray Flux (W/m²)", fontsize=11, fontweight='bold')
    plt.title("Aditya-L1 SoLEXS SDD2 to GOES Soft X-Ray Cross-Calibration", fontsize=12, fontweight='bold', pad=15)
    plt.grid(True, which="both", ls="-", alpha=0.15)
    plt.legend(loc="upper left", fontsize=9, framealpha=0.95)
    
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()
    print("Calibration plot saved successfully!")
    print("="*60)

if __name__ == "__main__":
    main()
