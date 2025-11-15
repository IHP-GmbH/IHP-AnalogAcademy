#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")   # Use non-GUI backend for batch plotting
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) < 2:
        print("Usage: python plot_diffout.py data.txt")
        sys.exit(1)

    filename = sys.argv[1]

    # Load data (two columns: time, differential output)
    data = np.loadtxt(filename)
    t = data[:, 0]
    y = data[:, 1]

    # Plot
    plt.figure(figsize=(8,5))
    plt.plot(t, y, label="Differential Output")
    plt.xlabel("Time (s)")
    plt.ylabel("Differential Output (V)")
    plt.title("Differential Output vs Time")
    plt.legend()
    plt.grid(True)

    # Save plot as PNG
    outname = filename.replace(".txt", ".png")
    plt.savefig(outname, dpi=300)
    plt.close()
    print(f"Saved plot as {outname}")

    # Estimate frequency using FFT
    # Compute sampling interval
    dt = np.mean(np.diff(t))
    fs = 1/dt  # sampling frequency

    # FFT
    Y = np.fft.fft(y - np.mean(y))  # remove DC component
    freqs = np.fft.fftfreq(len(Y), d=dt)

    # Only positive frequencies
    mask = freqs > 0
    freqs = freqs[mask]
    Y = np.abs(Y[mask])

    # Find frequency with maximum magnitude
    freq_peak = freqs[np.argmax(Y)]
    print(f"Estimated frequency: {freq_peak:.3e} Hz")

if __name__ == "__main__":
    main()
