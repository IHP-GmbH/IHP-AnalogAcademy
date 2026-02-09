import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import re

def read_snp(filename, num_ports):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Ignore comments and extract data
    data = []
    for line in lines:
        if not line.startswith('!') and not line.startswith('#'):
            data.append([float(x) for x in line.split()])

    data = np.array(data)
    freq = data[:, 0]  # Frequency in Hz
    s_params = data[:, 1:]  # S-parameters (real and imaginary parts)

    # Convert to complex numbers
    s_complex = s_params[:, 0::2] + 1j * s_params[:, 1::2]

    return freq, s_complex

def plot_and_save_s_parameters(freq, s_complex, num_ports, save_folder):
    s_db = 20 * np.log10(np.abs(s_complex))  # Convert to dB

    # Create the folder if it doesn't exist
    os.makedirs(save_folder, exist_ok=True)

    fig, axes = plt.subplots(num_ports, num_ports, figsize=(12, 10))  # NxN grid
    fig.suptitle("S-Parameters Magnitude (dB)")

    for i in range(num_ports):
        for j in range(num_ports):
            ax = axes[i, j] if num_ports > 1 else axes
            ax.plot(freq / 1e9, s_db[:, i * num_ports + j], label=f"S{i+1}{j+1}")
            ax.set_xlabel("Frequency (GHz)")
            ax.set_ylabel("Magnitude (dB)")
            ax.legend()
            ax.grid()

    plt.tight_layout()
    plt.savefig(os.path.join(save_folder, "s_parameters_db.png"))
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py your_file.sNp")
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    # Extract number of ports from filename (e.g., .s3p → 3)
    match = re.search(r'\.s(\d+)p$', filename)
    if not match:
        print("Error: Could not determine the number of ports from filename.")
        sys.exit(1)

    num_ports = int(match.group(1))

    save_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sparam_plots")
    freq, s_complex = read_snp(filename, num_ports)
    plot_and_save_s_parameters(freq, s_complex, num_ports, save_folder)

    print(f"Plots saved in: {save_folder}")

