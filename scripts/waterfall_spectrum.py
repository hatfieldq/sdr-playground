"""
Spectrum Analyzer with Waterfall Display - Version 2
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rtlsdr import RtlSdr
from collections import deque

CENTER_FREQ = 101.9e6
SAMPLE_RATE = 2.4e6
FFT_SIZE = 1024
NUM_SAMPLES = FFT_SIZE * 10
HISTORY_SIZE = 200          # Number of frames to keep from FFT

class WaterfallAnalyzer:
    def __init__(self):
        # Initialize SDR
        self.sdr = RtlSdr()
        self.sdr.sample_rate = SAMPLE_RATE
        self.sdr.center_freq = CENTER_FREQ
        self.sdr.gain = 'auto'

        # Setup dual plot
        self.fig, (self.ax_spectrum, self.ax_waterfall) = plt.subplots(
            2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [1, 2]}
        )

        self.freqs = np.fft.fftshift(np.fft.fftfreq(FFT_SIZE, 1/SAMPLE_RATE))
        self.freqs += CENTER_FREQ
        self.freqs_mhz = self.freqs / 1e6

        # Spectrum plot
        self.line, = self.ax_spectrum.plot(self.freqs_mhz, np.zeros(FFT_SIZE))
        self.ax_spectrum.set_xlabel('Frequency (MHz)')
        self.ax_spectrum.set_ylabel('Power(dB)')
        self.ax_spectrum.set_title(f'Real-time Spectrum - Center: {CENTER_FREQ/1e6:.1f} MHz')
        self.ax_spectrum.grid(True, alpha=0.3)
        self.ax_spectrum.set_ylim(-40, 60)

        # Waterfall plot
        self.waterfall_data = np.zeros((HISTORY_SIZE, FFT_SIZE))
        self.waterfall_img = self.ax_waterfall.imshow(
            self.waterfall_data,
            aspect='auto',
            cmap='viridis', 
            extent=[self.freqs_mhz[0], self.freqs_mhz[-1], HISTORY_SIZE, 0],
            vmin=-40,
            vmax=60
        )
        self.ax_waterfall.set_xlabel('Frequency (MHz)')
        self.ax_waterfall.set_ylabel('Time (frames)')
        self.ax_waterfall.set_title('Waterfall Display')

        # Add colorbar
        self.fig.colorbar(self.waterfall_img, ax=self.ax_waterfall, label='Power (dB)')

        plt.tight_layout()

    def compute_psd(self, samples):
        """Compute PSD"""
        windowed = samples * np.hanning(len(samples))
        fft_vals = np.fft.fft(windowed, FFT_SIZE)
        fft_vals = np.fft.fftshift(fft_vals)
        psd = 10 * np.log10(np.abs(fft_vals)**2 + 1e-10)
        return psd
    
    def update(self, frame):
        """Animation update function"""
        # Read samples
        samples = self.sdr.read_samples(NUM_SAMPLES)
        samples = samples[:FFT_SIZE]

        # Compute PSD
        psd = self.compute_psd(samples)

        # Update spectrum plot
        self.line.set_ydata(psd)

        # Update waterfall (scroll down)
        self.waterfall_data = np.roll(self.waterfall_data, 1, axis=0)
        self.waterfall_data[0, :] = psd
        self.waterfall_img.set_data(self.waterfall_data)

        return self.line, self.waterfall_img
    
    def run(self):
        """Start the analyzer"""
        anim =FuncAnimation(
            self.fig, 
            self.update, 
            interval=50, 
            blit=True,
            cache_frame_data=False
        )
        plt.show()
    
    def close(self):
        """Cleanup"""
        self.sdr.close()

if __name__ == '__main__':
    analyzer = WaterfallAnalyzer()
    try:
        analyzer.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        analyzer.close()
