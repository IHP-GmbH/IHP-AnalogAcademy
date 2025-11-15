#!/usr/bin/env python3
"""
pn_batch.py

Usage:
    python pn_batch.py data1.txt data2.txt ...

Input format:
    - Two columns: time[s]  v[t]
    - Three columns: time[s]  vp[t]  vn[t]  (script will use vp - vn)

Outputs:
    - ./spectrum/<basename>_phase_noise.png
    - printed summary: carrier freq estimate, fs (after resample), record length, samples
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, butter, filtfilt
from scipy.interpolate import interp1d

# --------- Parameters you can tweak ----------
RESAMPLE = True            # resample to uniform grid if input isn't uniform
TARGET_SAMPLES = 200000    # target samples when resampling (tradeoff mem / res)
LPF_BW = None              # if None, autopick based on carrier (see code). Bandwidth for baseband LPF (Hz)
NPERSEG = None             # if None, will choose based on record length (see code)
OVERLAP = 0.5              # fraction for Welch overlap
# ------------------------------------------------

def load_data(fname):
    data = np.loadtxt(fname)
    if data.ndim == 1 or data.shape[1] == 1:
        raise ValueError("File must have 2 or 3 columns (time, v) or (time, vp, vn)")
    t = data[:,0]
    if data.shape[1] == 2:
        v = data[:,1]
    else:
        v = data[:,1] - data[:,2]
    return t, v

def uniform_resample(t, v, target_samples=200000):
    # build uniform grid from min->max with target_samples (bounded)
    t0, t1 = float(t[0]), float(t[-1])
    dt_median = np.median(np.diff(t))
    if dt_median == 0:
        raise ValueError("Median dt is zero: check the input file for repeated timestamps.")
    N = min(target_samples, max(1024, int((t1 - t0) / dt_median)))
    tu = np.linspace(t0, t1, N)
    interp = interp1d(t, v, kind='cubic', bounds_error=False, fill_value="extrapolate")
    vu = interp(tu)
    return tu, vu

def estimate_carrier_freq(t, v, fs_est=None):
    # Quick FFT-based estimate (uses zero-padding for better resolution)
    N = len(t)
    i0, i1 = N//4, 3*N//4
    x = v[i0:i1] * np.hanning(i1-i0)
    nfft = 1 << (int(np.ceil(np.log2(len(x)))) + 3)
    X = np.fft.rfft(x, n=nfft)
    freqs = np.fft.rfftfreq(nfft, d=(t[1]-t[0]))
    mag = np.abs(X)
    idx = np.argmax(mag)
    # parabolic refine around peak
    if 1 <= idx < len(mag)-1:
        alpha = mag[idx-1]
        beta = mag[idx]
        gamma = mag[idx+1]
        p = 0.5*(alpha - gamma)/(alpha - 2*beta + gamma)
        peak_freq = (freqs[idx] + p*(freqs[1]-freqs[0]))
    else:
        peak_freq = freqs[idx]
    return peak_freq

def lowpass_iq(t, v, fc, fs_bb):
    # Mix down to baseband using the estimated fc, then lowpass to fs_bb/2
    t = np.asarray(t)
    carrier = 2*np.pi*fc*t
    I = v * np.cos(carrier)
    Q = -v * np.sin(carrier)

    nyq = 0.5 * (1.0/(t[1]-t[0]))
    cutoff = min(0.5*fs_bb, nyq*0.9)
    b, a = butter(4, cutoff/nyq)
    I_f = filtfilt(b, a, I)
    Q_f = filtfilt(b, a, Q)

    t_start, t_end = t[0], t[-1]
    num = int(np.floor((t_end - t_start) * fs_bb))
    if num < 16:
        raise ValueError("fs_bb too high or record too short for downsampling. Decrease fs_bb.")
    tb = np.linspace(t_start, t_end, num)
    I_interp = interp1d(t, I_f, kind='cubic')(tb)
    Q_interp = interp1d(t, Q_f, kind='cubic')(tb)
    return tb, I_interp, Q_interp

def compute_phase_from_iq(I, Q):
    phase = np.unwrap(np.arctan2(Q, I))
    return phase

def phase_to_LdBcHz(phase, fs_bb, nperseg=None, overlap=0.5):
    if nperseg is None:
        nperseg = min(len(phase), 2**14)
    noverlap = int(nperseg * overlap)
    f, Pphi = welch(phase, fs=fs_bb, nperseg=nperseg, noverlap=noverlap, scaling='density', window='hann')
    L = 10*np.log10(0.5 * Pphi)
    return f, L

def process_file(fname):
    fname = Path(fname)
    t, v = load_data(fname)
    sort_idx = np.argsort(t)
    t = t[sort_idx]
    v = v[sort_idx]

    if RESAMPLE:
        t_u, v_u = uniform_resample(t, v, target_samples=TARGET_SAMPLES)
    else:
        dt = np.diff(t)
        if np.max(dt) - np.min(dt) > 1e-12:
            t_u, v_u = uniform_resample(t, v, target_samples=TARGET_SAMPLES)
        else:
            t_u, v_u = t, v

    dt = t_u[1] - t_u[0]
    fs = 1.0 / dt
    T = t_u[-1] - t_u[0]

    fc = estimate_carrier_freq(t_u, v_u, fs_est=fs)

    if LPF_BW is None:
        fs_bb = min(1e6, max(200000.0, fs/20))
    else:
        fs_bb = max(1000.0, LPF_BW*4)

    nyq_orig = 0.5*fs
    if fs_bb > nyq_orig*0.9:
        fs_bb = nyq_orig*0.9

    try:
        tb, Ibb, Qbb = lowpass_iq(t_u, v_u, fc, fs_bb)
    except Exception as e:
        raise RuntimeError("IQ demod failed: " + str(e))

    phase = compute_phase_from_iq(Ibb, Qbb)
    p = np.polyfit(tb, phase, 1)
    phase_dev = phase - np.polyval(p, tb)

    if NPERSEG is None:
        nperseg = int(max(256, min(len(phase_dev), int(fs_bb * (T/8.0)))))
        nperseg = 1 << int(np.floor(np.log2(nperseg)))
    else:
        nperseg = NPERSEG

    f, L = phase_to_LdBcHz(phase_dev, fs_bb, nperseg=nperseg, overlap=OVERLAP)

    outdir = Path("spectrum")
    outdir.mkdir(parents=True, exist_ok=True)
    out_png = outdir / (fname.stem + "_phase_noise.png")

    plt.figure(figsize=(6.5,4))
    plt.semilogx(f, L)
    plt.xlim(max(1.0, f[1]), f[-1])
    plt.xlabel("Offset frequency [Hz]")
    plt.ylabel("Phase noise [dBc/Hz]")
    plt.title(f"{fname.name}  fc~{fc/1e6:.6f} MHz  fs_bb={fs_bb/1e3:.1f} kHz  T={T*1e6:.3f} µs")
    plt.grid(True, which='both', ls=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()

    print(f"{fname.name}: fc={fc:.3f} Hz, fs={fs:.1f} Hz, T={T:.6f} s, samples={len(t_u)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python pn_batch.py data1.txt data2.txt ...")
        sys.exit(1)
    for f in sys.argv[1:]:
        try:
            process_file(f)
        except Exception as e:
            print(f"Error processing {f}: {e}")

if __name__ == "__main__":
    main()
