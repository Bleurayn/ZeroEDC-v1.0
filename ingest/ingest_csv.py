import pandas as pd
import numpy as np

def ingest_public_csv(file_path):
    df = pd.read_csv(file_path)
    # Simulate real-world mess
    df.iloc[::10, 1] = np.nan
    df.iloc[::20, 1] += np.random.normal(0, 2)
    return df
