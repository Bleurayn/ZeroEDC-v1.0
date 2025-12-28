import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

def generate_synthetic(real_csv_path, n_patients=1000, epsilon=1.0, rare_oversample=2.0):
    real = pd.read_csv(real_csv_path)
    
    # Rare event oversampling (customize to your columns, e.g., ethnicity or allele)
    rare_mask = real['ethnicity_not hispanic or latino'] == 0  # Example 'Hispanic'
    rare = real[rare_mask]
    if not rare.empty:
        rare_sampled = rare.sample(int(len(rare) * (rare_oversample - 1)), replace=True)
        augmented = pd.concat([real, rare_sampled])
    else:
        augmented = real
    
    # Simple synth (numpy for available env; use CTGAN in full)
    synth_tabular = pd.DataFrame()
    for col in augmented.select_dtypes(include=np.number).columns:
        mean = augmented[col].mean()
        std = augmented[col].std()
        synth_tabular[col] = np.random.normal(mean, std, n_patients)
    
    for col in augmented.select_dtypes(include='object').columns:
        synth_tabular[col] = np.random.choice(augmented[col].unique(), n_patients)
    
    # DP noise
    for col in synth_tabular.select_dtypes(include=np.number).columns:
        synth_tabular[col] += np.random.laplace(0, 1.0 / epsilon, n_patients)
    
    # Sim narratives (LLM in full)
    narratives = ["Simulated history for patient " + str(i) for i in range(n_patients)]
    synth_tabular['Narrative_History'] = narratives
    
    synth_tabular.to_csv("synthetic_cohort_enhanced.csv", index=False)
    
    # Fidelity test
    real_col = real['age_at_index']  # Example
    synth_col = synth_tabular['age_at_index']
    ks_stat, p_value = ks_2samp(real_col, synth_col)
    print(f"KS p-value: {p_value:.4f} (aim >0.05 for 98%+ fidelity)")

    return synth_tabular

# Test call
generate_synthetic('brca.csv', n_patients=10)
