import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_images(csv_path, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Reading data from {csv_path}...")
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: Could not find {csv_path}.")
        print("Please wait for the background extraction script to finish generating the CSV.")
        return

    # Define the parameters to plot and their corresponding y-axis labels and titles
    parameters = [
        {'col': 'Temperature_val', 'ylabel': 'Temperature (keV)', 'title': 'Time Evolution of Plasma Temperature'},
        {'col': 'dT_dt', 'ylabel': 'dT/dt (keV/s)', 'title': 'Rate of Change of Plasma Temperature'},
        {'col': 'Emission_Measure_norm', 'ylabel': 'Emission Measure (norm)', 'title': 'Time Evolution of Emission Measure'},
        {'col': 'dEM_dt', 'ylabel': 'dEM/dt (norm/s)', 'title': 'Rate of Change of Emission Measure'},
        {'col': 'Spectral_Index_Gamma', 'ylabel': 'Spectral Index (\gamma)', 'title': 'Time Evolution of Spectral Index'},
        {'col': 'dGamma_dt', 'ylabel': 'd\gamma/dt (s^{-1})', 'title': 'Rate of Change of Spectral Index'},
        {'col': 'Hardness_Ratio', 'ylabel': 'Hardness Ratio (Hard/Soft)', 'title': 'Time Evolution of Hardness Ratio'},
        {'col': 'dHR_dt', 'ylabel': 'd(HR)/dt (s^{-1})', 'title': 'Rate of Change of Hardness Ratio'}
    ]

    # Create a time axis if it's just bin numbers
    time_axis = df['Time_Bin']

    # Set up plot styling
    plt.style.use('seaborn-v0_8-darkgrid')
    
    print(f"Generating {len(parameters)} plots...")
    for param in parameters:
        col = param['col']
        if col not in df.columns:
            print(f"Warning: Column {col} not found in CSV. Skipping...")
            continue
            
        plt.figure(figsize=(10, 6))
        plt.plot(time_axis, df[col], label=col, color='tab:blue', linewidth=1.5)
        
        plt.title(param['title'], fontsize=14, fontweight='bold')
        plt.xlabel('Time (Seconds / Bin Number)', fontsize=12)
        plt.ylabel(param['ylabel'], fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Save to the output directory
        filename = f"{col}_evolution.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300)
        plt.close()
        print(f"Saved: {filepath}")

    print("All images generated successfully!")

if __name__ == "__main__":
    CSV_FILE = "/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed/AL1_SOLEXS_SDD2_L1_time_resolved_params.csv"
    OUTPUT_FOLDER = "/Users/aditya1981/Documents/Unified Data Ingestion Engine/data/processed/spectral_fitting_images"
    
    generate_images(CSV_FILE, OUTPUT_FOLDER)
