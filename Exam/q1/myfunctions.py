from scipy.signal import butter, lfilter
import numpy as np

MAXVALUE = 2**15-1

# generate a, b parameters
def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandpass')
    return b, a

# bandpass filter
def bandpass_filter(data, center, fs, states, order=2):
    # generate lowcut and highcut
    lowcut = center - 300
    highcut = center + 300
    # generate a, b
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    [y, states] = lfilter(b, a, data, zi=states)
    # normalize the output
    y = np.clip(y, -MAXVALUE, MAXVALUE)
    # transform the type of output to int
    y = y.astype(int)
    return [y, states]

