import subprocess
import sys
from pathlib import Path

# List of dates with X-class and high-intensity M-class solar flares
# that have matching processed telemetry files (merged_*.parquet) in the workspace
FLARE_DATES = [
    # X-Class Flares
    "2024-02-12",
    "2024-08-01",
    "2024-09-12",
    "2025-01-03",
    "2025-06-19",
    "2025-12-01",
    
    # High-intensity M-Class Flares
    "2024-07-31",
    "2024-08-14",
    "2024-09-13",
    "2024-10-18",
    "2024-11-04",
    "2025-02-23",
    "2025-04-01",
    "2025-06-16",
    "2026-04-24",
    "2026-04-26",
    
    # Quiet Sun (No flares)
    "2024-07-30",
    "2024-12-18",
    "2025-02-27",
    "2025-10-02",
    "2025-10-04",
    "2025-10-05",
    "2025-10-07",
    "2025-10-08",
    "2025-10-09",
    "2025-10-10",
    
    # C-Class Flare Dates
    "2024-07-07",
    "2024-07-10",
    "2024-08-12",
    "2024-08-15",
    "2024-08-17",
    "2024-08-18",
    "2024-08-19",
    "2024-08-20",
    "2024-09-11",
    "2024-10-11",
    
    # A/B-Class Flare Dates
    "2024-07-01",
    "2024-07-06",
    "2024-07-08",
    "2024-07-17",
    "2024-07-18",
    "2024-07-19",
    "2024-07-20",
    "2024-07-21"
]

def main():
    print("="*60)
    print("      Aditya-L1 aligned GOES Flare Dataset Ingestor")
    print("="*60)
    print(f"Targeting {len(FLARE_DATES)} high-occurrence flare dates...")
    
    python_exe = sys.executable
    downloader_script = Path(__file__).parent / "goes_downloader.py"
    
    for idx, date in enumerate(FLARE_DATES, 1):
        # Dynamically choose satellite: GOES-18 for dates after April 2025
        # (since GOES-16 science L1b data stops in April 2025 on NOAA NCEI archive)
        satellite = "goes18" if date >= "2025-05-01" else "goes16"
        print(f"\n[{idx}/{len(FLARE_DATES)}] Launching download/parsing for: {date} using {satellite}")
        cmd = [
            python_exe,
            str(downloader_script),
            "--start", date,
            "--end", date,
            "--satellite", satellite,
            "--cadence", "1min"
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            # Print last few lines of output
            lines = result.stdout.strip().split('\n')
            summary_lines = [l for l in lines if "saved" in l or "flux" in l or "Completed" in l or "Processed" in l]
            for l in summary_lines:
                print(f"  {l}")
        except subprocess.CalledProcessError as e:
            print(f"Error running downloader for {date}:")
            print(e.stderr)
            
    print("\n" + "="*60)
    print("Multi-date GOES Ingestion Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
