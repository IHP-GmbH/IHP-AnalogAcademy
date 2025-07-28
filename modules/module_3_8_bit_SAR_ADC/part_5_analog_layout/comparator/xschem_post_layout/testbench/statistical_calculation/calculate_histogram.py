import numpy as np
import sys
import os
import matplotlib.pyplot as plt

SI_PREFIXES = {
    -9: "n",  # nano
    -6: "µ",  # micro
    -3: "m",  # milli
     0: "",   # base unit
     3: "k",  # kilo
     6: "M",  # Mega
     9: "G"   # Giga
}

def get_best_unit(value):
    if value == 0:
        return 0, ""
    exponent = int(np.floor(np.log10(abs(value)) / 3) * 3)
    exponent = max(min(exponent, 9), -9)
    unit = SI_PREFIXES.get(exponent, "")
    return exponent, unit

def format_value(value):
    exponent, unit = get_best_unit(value)
    return f"{value / (10**exponent):.6g} {unit}"

def calculate_histogram_data(file_path):
    results = []
    errors_removed = 0
    total_samples = 0
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith("Index") or not line.strip():
                    continue
                
                try:
                    _, result = line.split()
                    value = float(result)
                    total_samples += 1  # Count total samples

                    # Check if value is exactly 1.0000e+00
                    if value == 1.0:
                        errors_removed += 1
                        continue  # Skip this value

                    results.append(value)
                except ValueError:
                    continue
    except Exception as e:
        print(f"Error reading the file: {e}")
        return [], 0, 0, errors_removed, total_samples
    
    if errors_removed > 0:
        print(f"ERROR: There are {errors_removed} values out of bounds (equal to 1.0), data has been removed.")
        print(f"Total samples: {total_samples}, Remaining samples: {total_samples - errors_removed}")
    else:
        print(f"Total samples: {total_samples}")
    
    mean = np.mean(results)
    std_dev = np.std(results)
    
    print(f"Mean: {format_value(mean)}")
    print(f"Standard Deviation: {format_value(std_dev)}")
    
    return results, mean, std_dev, errors_removed, total_samples

def create_histogram(results, mean, std_dev):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    histogram_dir = os.path.join(script_directory, "histogram_plots")

    if not os.path.exists(histogram_dir):
        os.makedirs(histogram_dir)

    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot histogram
    bins = 30
    counts, bin_edges, _ = ax.hist(results, bins=bins, edgecolor='black', color='skyblue', alpha=0.7)

    # Overlay individual data points as scatter dots
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    jitter = np.random.uniform(-0.1, 0.1, size=len(results))  # Adds slight randomness to prevent overlap
    ax.scatter(results, np.random.uniform(0, counts.max() * 0.1, len(results)), 
               color='red', s=15, alpha=0.7, label=f"Mean: {format_value(mean)}\nStd Dev: {format_value(std_dev)}")

    # Title and labels
    ax.set_title('Histogram of Results', fontsize=16, fontweight='bold')
    ax.set_xlabel('Results', fontsize=14)
    ax.set_ylabel('Frequency', fontsize=14)

    # Grid settings
    ax.grid(True, linestyle='--', alpha=0.5)

    # Set ticks for better readability
    ax.tick_params(axis='both', which='major', labelsize=12)

    # Save figure
    histogram_path = os.path.join(histogram_dir, "histogram.png")
    plt.legend()
    plt.tight_layout()
    plt.savefig(histogram_path, dpi=300)
    print(f"Histogram saved to {histogram_path}")
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_txt_file>")
    else:
        file_path = sys.argv[1]

        results, mean, std_dev, errors_removed, total_samples = calculate_histogram_data(file_path)

        if results:
            generate_histogram = input("Do you want to create a histogram plot? (y/n): ").strip().lower()
            if generate_histogram == 'y':
                create_histogram(results, mean, std_dev)
