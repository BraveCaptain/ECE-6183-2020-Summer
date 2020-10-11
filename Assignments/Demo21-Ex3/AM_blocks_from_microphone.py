# AM_from_microphone.py
# Record audio and play it with amplitude modulation. 
# This implementation:
#   uses blocking, 
#   corrects for block-to-block angle mismatch,
#   assumes mono channel
# Original by Gerald Schuller, 2013


import pyaudio
import struct
import math
import cmath
from matplotlib import pyplot
import scipy
from scipy import signal
from myfunctions import clip16

# f0 = 0      # Normal audio
f0 = 400    # Modulation frequency (Hz)

BLOCKLEN = 1024      # Number of frames per block
WIDTH = 2           # Number of bytes per signal value
CHANNELS = 1        # mono
RATE = 32000        # Frame rate (frames/second)
RECORD_SECONDS = 5
theta = 0
om = 1 / RATE
p = pyaudio.PyAudio()

stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)

K = 7
[b_lpf, a_lpf] = scipy.signal.ellip(K, 0.2, 50, 0.48)
I = 1j
s = [1+1j] * (K+1)
a = [1+1j] * (K+1)
b = [1+1j] * (K+1)
for i in range (K+1):
    s[i] = cmath.exp(I * 0.5 * cmath.pi * i)
    s[i] = round(s[i].real) + round(s[i].imag) * 1j
    a[i] = a_lpf[i] * s[i]
    b[i] = b_lpf[i] * s[i]
output_block = BLOCKLEN * [0]


# Number of blocks to run for
num_blocks = int(RATE / BLOCKLEN * RECORD_SECONDS)

print('* Recording for %.3f seconds' % RECORD_SECONDS)
# Start loop
for i in range(0, num_blocks):

    # Get frames from audio input stream
    input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)   # BLOCKLEN = number of frames read

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)
    
    # Go through block
    R = signal.lfilter(b, a, input_tuple)
    #print(R)
    for r in R:
        theta = theta + om
        g = r * cmath.exp(I * 2 * cmath.pi * f0 * theta)
        while theta > math.pi:
            theta = theta - 2 * cmath.pi
        y = clip16(int(g.real))
        output_byte = struct.pack('h', y)
        stream.write(output_byte)


print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
