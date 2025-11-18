from typing import Any
import numpy as np

def postprocess(results: dict[str, list], conditions: dict[str, Any]) -> dict[str, list]:
    # Extract waveform
    t = np.array(results['time'])
    v = np.array(results['vo_diff'])

    if len(t) < 2 or len(v) == 0:
        return {
            'frequency': [0.0],
            'amplitude': [0.0],
            'voltage_swing': [0.0]
        }

    # --- Compute sampling frequency ---
    dt = np.mean(np.diff(t))
    fs = 1.0 / dt

    # --- FFT to find main tone ---
    Y = np.fft.fft(v - np.mean(v))  # remove DC
    freqs = np.fft.fftfreq(len(Y), d=dt)

    # Use positive frequencies only
    mask = freqs > 0
    freqs = freqs[mask]
    Y = np.abs(Y[mask])

    freq_peak = freqs[np.argmax(Y)]

    # --- Compute amplitude and voltage swing ---
    v_max = np.max(v)
    v_min = np.min(v)
    voltage_swing = v_max - v_min
    amplitude = voltage_swing / 2.0

    return {
        'frequency': [freq_peak],
        'amplitude': [amplitude],
        'voltage_swing': [voltage_swing]
    }
