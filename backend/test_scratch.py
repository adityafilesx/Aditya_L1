import pandas as pd
import numpy as np

unix_in = np.array([1707715800, 1707802200])
dt = pd.to_datetime(unix_in, unit='s', utc=True)
print("total_seconds:", (dt - pd.Timestamp("1970-01-01", tz="UTC")).total_seconds())

