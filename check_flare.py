import pandas as pd
import numpy as np

f = "data/processed/merged_20250212.parquet"
try:
    df = pd.read_parquet(f)
    time_cols = [c for c in df.columns if "time" in c.lower() or "utc" in c.lower()]
    df[time_cols[0]] = pd.to_datetime(df[time_cols[0]])
    mask = ((df[time_cols[0]].dt.hour == 3) & (df[time_cols[0]].dt.minute >= 23)) | ((df[time_cols[0]].dt.hour == 4) & (df[time_cols[0]].dt.minute <= 10))
    sub = df[mask]
    counts = sub["solexs_sdd2_ctr"] if "solexs_sdd2_ctr" in sub.columns else sub.iloc[:, 1]
    
    print("Max count in 03:23-04:10 range:", counts.max())
    print("Mean count outside that range:", df[~mask]["solexs_sdd2_ctr"].mean() if "solexs_sdd2_ctr" in df.columns else np.nan)
    print("Mean count inside that range:", counts.mean())
except Exception as e:
    print(e)
