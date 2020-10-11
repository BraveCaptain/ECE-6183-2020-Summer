from scipy.signal import butter, lfilter
import numpy as np

MAXVALUE = 2**15-1

def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandpass')
    #print(a, " ", b)
    return b, a

def bandpass_filter(data, center, fs, states, bandwidth, order=2):
    lowcut = center - bandwidth / 2
    highcut = center + bandwidth / 2
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    [y, states] = lfilter(b, a, data, zi=states)
    y = np.clip(y, -MAXVALUE, MAXVALUE)
    y = y.astype(int)
    return [y, states]


