"""
Basic Spectrum Analyzer - Version 1
Displays real-time FFT of SDR input
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rtlsdr import RtlSdr

# Configuration
CENTER_FREQ = 1090e6
SAMPLE_RATE = 2.4e6
FFT_SIZE = 1024            # number of FFT bins
NUM_SAMPS = FFT_SIZE * 10   # samples per update

class SpectrumAnalyzer:
    def __init__(self):
        # Initialize SDR
        self.sdr = RtlSdr()
        self.sdr.sample_rate = SAMPLE_RATE
        self.sdr.center_freq = CENTER_FREQ
        self.sdr.gain = 50#'auto'

        # Setup plot 
        self.fig, self.ax = plt.subplots(figsize=(12,6))
        self.freqs = np.fft.fftshift(np.fft.fftfreq(FFT_SIZE, 1/SAMPLE_RATE))
        self.freqs += CENTER_FREQ           # shift to carrier frequency

        # Convert to MHz for display ease
        self.freqs_mhz = self.freqs / 1e6

        # Initialize line plot
        self.line, = self.ax.plot(self.freqs_mhz, np.zeros(FFT_SIZE))

        self.ax.set_xlabel('Frequency (MHz)')
        self.ax.set_ylabel('Power (dB)')
        self.ax.set_title(f'Spectrum Analyzer - Center: {CENTER_FREQ/1e6}')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_ylim(-80, 80)

    def compute_psd(self, samples):
        """Compute Power Spectral Density"""
        # Apply Hanning window to reduce spectral leakage
        windowed = samples * np.hanning(len(samples))

        # Compute FFT
        fft_vals = np.fft.fft(windowed, FFT_SIZE)
        fft_vals = np.fft.fftshift(fft_vals)            # Shift to carrier

        # Convert to power (dB)
        psd = 10 * np.log10(np.abs(fft_vals)**2 + 1e-10)

        return psd
    
    def update(self, samples):
        """Animation update function"""
        # Read samples from SDR
        samples = self.sdr.read_samples(NUM_SAMPS)
        
        # Take subset for FFT
        samples = samples[:FFT_SIZE]

        # Compute PSD
        psd = self.compute_psd(samples)

        # Update plot
        self.line.set_ydata(psd)

        return self.line,

    def run(self):
        """Start the spectrum analyzer"""
        anim = FuncAnimation(
            self.fig, 
            self.update,
            interval=50,        # update every 50 ms
            blit=True,
            cache_frame_data=False
        )
        plt.show()

    def close(self):
        """Cleanup"""
        self.sdr.close()

if __name__ == '__main__':
    analyzer = SpectrumAnalyzer()
    try:
        analyzer.run()
    except KeyboardInterrupt:
        print("\nShutting down ...")
    finally:
        analyzer.close()