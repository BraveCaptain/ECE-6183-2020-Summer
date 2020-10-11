# echo_via_circular_buffer.py
# Reads a specified wave file (mono) and plays it with an echo.
# This implementation uses a circular buffer.

import pyaudio
import wave
import struct
import numpy as np
from myfunctions import clip16


WIDTH = 2          # Bytes per sample
CHANNELS = 1       # Number of channels
RATE = 8000        # Sampling rate in Hz (samples/second)
DURATION = 2

K = 0.93
N = 60


a1 = 1
a61 = -K/2
a62 = -K/2
b0 = 1

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True)


# Buffer to store past signal values. Initialize to zero.
y61 = (N+1) * [0]
y62 = (N+2) * [0]

# Initialize buffer index (circular index)
k_61 = 0
k_62 = 0

print('* Start')
x = [0] * (DURATION * RATE + N)
for i in range (N):
    x[i] = np.random.randn() * 10000
for i in range(DURATION * RATE + N):
#for i in range(N):
    x0 = x[i]
    #print(x0)
    # Compute output value
    # y(n) = b0 x(n) - a61 y(n-61) - a62 y(n-62)
    y0 = b0*x0 - a61*y61[k_61] - a62*y62[k_62]
    # Update buffer
    y61[k_61] = y0
    y62[k_62] = y0

    # Increment buffer index
    k_61 += 1
    k_62 += 1
    if k_61 >= N+1:
        k_61 = 0
    if k_62 >= N+2:
        k_62 = 0
    # Clip and convert output value to binary data
    output_bytes = struct.pack('h', int(clip16(y0)))

    # Write output value to audio stream
    stream.write(output_bytes)
   
print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
