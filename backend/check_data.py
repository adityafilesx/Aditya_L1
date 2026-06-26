import pandas as pd
import json

f = "data/processed/merged_20250212.json"
print("Checking", f)
try:
    with open(f, 'r') as file:
        data = json.load(file)
        if isinstance(data, list) and len(data) > 0:
            keys = list(data[0].keys())
            print("Keys:", keys)
            time_cols = [k for k in keys if "time" in k.lower() or "utc" in k.lower()]
            if time_cols:
                times = [row.get(time_cols[0]) for row in data]
                print(min(times), "to", max(times))
        elif isinstance(data, dict):
            keys = list(data.keys())
            print("Keys:", keys)
            time_cols = [k for k in keys if "time" in k.lower() or "utc" in k.lower()]
            if time_cols:
                times = list(data[time_cols[0]].values())
                print(min(times), "to", max(times))
except Exception as e:
    print("Error", e)
