import numpy as np

def synth_dicom(real_dicom_path, output_path='synthetic.npy', noise_level=10):
    # Sim image (numpy array)
    pixel_array = np.ones((512,512)) * 128  # Sim 512x512 image
    pixel_array += np.random.normal(0, noise_level, pixel_array.shape)
    np.save(output_path, pixel_array)
    print("Synthetic image generated.")

def synth_vcf(real_df, output_vcf='synthetic.vcf', rare_allele_prob=0.05):
    with open(output_vcf, 'w') as f:
        f.write("# Sim VCF header\n")
        for i in range(len(real_df)):
            alt = 'A' if np.random.rand() < rare_allele_prob else 'G'
            f.write(f"chr1\t{i*100}\t.\tC\t{alt}\t99\t.\n")
    print("Synthetic VCF generated.")

# Test call
synth_dicom('sample.npy')
synth_vcf(pd.read_csv('brca.csv'))
