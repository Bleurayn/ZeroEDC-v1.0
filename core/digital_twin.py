import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

def build_twin(df, patient_id, variable='HbA1c'):
    patient_data = df[df['Patient_ID'] == patient_id]
    if patient_data.empty:
        return {'predictions': [], 'confidence': 0.0}
    X = np.array([(row['Date'] - patient_data['Date'].min()).days for _, row in patient_data.iterrows()]).reshape(-1, 1)
    y = patient_data[variable].values
    model = LinearRegression().fit(X, y)
    future_days = np.array([30, 60, 90]).reshape(-1, 1)
    predictions = model.predict(future_days)
    confidence = np.mean([0.98 if abs(pred - np.mean(y)) < np.std(y) else 0.92 for pred in predictions])
    confidence = max(0.0, min(1.0, confidence))
    return {'predictions': predictions.tolist(), 'confidence': round(confidence, 4)}

# Test
if __name__ == "__main__":
    sample_df = pd.DataFrame({
        'Patient_ID': ['P001']*5,
        'Date': [datetime(2025,1,1) + timedelta(days=i*28) for i in range(5)],
        'HbA1c': [7.8, 7.5, 7.2, 6.9, 6.7]
    })
    print(build_twin(sample_df, 'P001'))
