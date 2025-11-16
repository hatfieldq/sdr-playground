import numpy as np
from scipy.signal import decimate
import sounddevice as sd

# Load Samples
samples = np.load('data/iq_samples/fm_station101o9.npy')

# FM Demodulation
phase = np.angle(samples)
diff = np.diff(phase)
audio = np.unwrap(diff)

# Downsample to audio range
audio = decimate(audio, 48)

# Normalize volume
audio = audio / np.max(np.abs(audio))

print("Playing audio...")
sd.play(audio, 48000)
sd.wait()
