import numpy as np
from scipy.signal import butter, filtfilt

def analyze_yaw_rate(yaw_rate_signal, sampling_rate=20, window_size=1):
    # Apply a low-pass filter to remove high-frequency noise
    nyquist = 0.5 * sampling_rate
    cutoff = 2  # 2 Hz cutoff frequency
    b, a = butter(4, cutoff / nyquist, btype='low')
    filtered_signal = filtfilt(b, a, yaw_rate_signal)
    
    # Reshape the signal into 1-second chunks
    samples_per_window = window_size * sampling_rate
    windows = len(filtered_signal) // samples_per_window
    reshaped_signal = filtered_signal[:windows * samples_per_window].reshape(windows, samples_per_window)
    
    # Calculate statistics for each window
    mean_yaw_rates = np.mean(reshaped_signal, axis=1)
    max_yaw_rates = np.max(np.abs(reshaped_signal), axis=1)
    std_yaw_rates = np.std(reshaped_signal, axis=1)
    
    # Determine vehicle behavior for each window
    behavior = []
    for mean, max_rate, std in zip(mean_yaw_rates, max_yaw_rates, std_yaw_rates):
        if std > 0.1 and max_rate < 0.3:
            behavior.append("Wobbling")
        elif abs(mean) > 0.2 and max_rate > 0.5:
            behavior.append("Turning")
        elif abs(mean) > 0.05 and max_rate > 0.2:
            behavior.append("Overtaking")
        else:
            behavior.append("Stable")
    # return behavior, mean_yaw_rates, max_yaw_rates, std_yaw_rates
    return behavior
