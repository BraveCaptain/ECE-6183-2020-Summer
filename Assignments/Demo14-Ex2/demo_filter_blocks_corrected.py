# demo_filter_blocks_corrected.py
# Block filtering of a wave file, save the output to a wave file.
# Corrected version.

import pyaudio, wave, struct, math
import numpy as np
import scipy.signal
from matplotlib import pyplot

wavfile = 'author.wav'
output_wavfile = 'author_output_blocks_corrected.wav'

print('Play the wave file %s.' % wavfile)

# Open wave file (should be mono channel)
wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
CHANNELS        = 1     # Number of channels
RATE            = 32000     # Sampling rate (frames/second)
WIDTH           = 2     # Number of bytes per sample
DURATION        = 5

# Difference equation coefficients
b0 =  0.008442692929081
b2 = -0.016885385858161
b4 =  0.008442692929081
b = [b0, 0.0, b2, 0.0, b4]

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 =  4.942669993770672
a3 = -3.114402101627517
a4 =  0.757546944478829
a = [1.0, a1, a2, a3, a4]

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True )

BLOCKLEN = 512
MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Set up plotting...

pyplot.ion()           # Turn on interactive mode
pyplot.figure(1)
[g1] = pyplot.plot([], [], 'blue', label='input signal')
[g2] = pyplot.plot([], [], 'green', label='output signal')

n = range(0, BLOCKLEN)
pyplot.xlim(0, BLOCKLEN)         # set x-axis limits
pyplot.xlabel('Time (n)')
g1.set_xdata(n)      
g2.set_xdata(n)              # x-data of plot (discrete-time)
pyplot.ylim(-10000, 10000)        # set y-axis limits
pyplot.legend()


ORDER = 4   # filter is fourth order
states = np.zeros(ORDER)
num_blocks = int (RATE * DURATION / BLOCKLEN)
for i in range (0, num_blocks):
    input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)   # BLOCKLEN = number of frames read
    # convert binary data to numbers
    input_block = struct.unpack('h' * BLOCKLEN, input_bytes)

    # filter
    [output_block, states] = scipy.signal.lfilter(b, a, input_block, zi = states)

    # clipping
    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)

    # convert to integer
    output_block = output_block.astype(int)

    g1.set_ydata(input_block)   # Update y-data of plot
    g2.set_ydata(output_block)   # Update y-data of plot
    pyplot.pause(0.00001)
    

    # Convert output value to binary data
    output_bytes = struct.pack('h' * BLOCKLEN, *output_block)
    stream.write(output_bytes)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()

# Close wavefiles
wf.close()
output_wf.close()
