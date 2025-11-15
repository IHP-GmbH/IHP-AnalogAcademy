from typing import Any
import numpy as np

def postprocess(results: dict[str, list], conditions: dict[str, Any]) -> dict[str, list]:
    # Extract waveform
    t = np.array(results['time_axis'])
    y = np.array(results['vo_diff'])

    if len(y) == 0:
        # Fallback if waveform is empty
        return {'frequency': [0.0]}

    dt = np.mean(np.diff(t))
    fs = 1 / dt

    # FFT
    Y = np.fft.fft(y - np.mean(y))  # remove DC
    freqs = np.fft.fftfreq(len(Y), d=dt)

    # Only positive frequencies
    mask = freqs > 0
    freqs = freqs[mask]
    Y = np.abs(Y[mask])

    # Find frequency with maximum magnitude
    freq_peak = freqs[np.argmax(Y)]  # convert to GHz


    # Return as a list for compatibility with sweep/postprocessing tools
    return {'frequency': [freq_peak]}
