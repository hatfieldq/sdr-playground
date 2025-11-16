from rtlsdr import RtlSdr
import numpy as np

sdr = RtlSdr()

# Configure SDR
sdr.sample_rate = 2.4e6;
sdr.center_freq = 101.9e6;
sdr.gain = 'auto';

# Save samples to file
samples = sdr.read_samples(10*256*1024)
samples = np.array(samples, dtype=np.complex64)

# Save to file
np.save('data/iq_samples/fm_station101o9.npy', samples)

sdr.close()
print("Saved samples to data/iq_samples/fm_station101o9.npy")
