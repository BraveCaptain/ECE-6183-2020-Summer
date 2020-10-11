# plot_microphone_input_spectrum.py

"""
Using Pyaudio, get audio input and plot real-time FFT of blocks.
Ivan Selesnick, October 2015
Based on program by Gerald Schuller
"""

import pyaudio
import struct
from matplotlib import pyplot as plt
import numpy as np
import math

plt.ion()           # Turn on interactive mode so plot gets updated

WIDTH     = 2         # bytes per sample
CHANNELS  = 1         # mono
RATE      = 8000     # Sampling rate (samples/second)
BLOCKSIZE = 1024      # length of block (samples)
DURATION  = 30        # Duration (seconds)

NumBlocks = int( DURATION * RATE / BLOCKSIZE )

print('BLOCKSIZE =', BLOCKSIZE)
print('NumBlocks =', NumBlocks)
print('Running for ', DURATION, 'seconds...')

# Initialize phase
f0 = 500
om = 2*math.pi*f0/RATE
theta = 0

DBscale = False
# DBscale = True

# Initialize plot window:
plt.figure(1)
if DBscale:
    plt.ylim(0, 150)
else:
    plt.ylim(0, 20*RATE)

# Frequency axis (Hz)
plt.xlim(0, 0.5*RATE)         # set x-axis limits
# plt.xlim(0, 2000)         # set x-axis limits
plt.xlabel('Frequency (Hz)')
f = RATE/BLOCKSIZE * np.arange(0, BLOCKSIZE)

[line1] = plt.plot([], [], color = 'blue')  
line1.set_xdata(f)                        
[line2] = plt.plot([], [], color = 'red')  
line2.set_xdata(f)                        

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)

stream = p.open(
    format    = PA_FORMAT,
    channels  = CHANNELS,
    rate      = RATE,
    input     = True,
    output    = True)

output_block = BLOCKSIZE * [0]

for i in range(0, NumBlocks):
    input_bytes = stream.read(BLOCKSIZE)                     # Read audio input stream
    input_tuple = struct.unpack('h' * BLOCKSIZE, input_bytes)  # Convert
	# Go through block
    for n in range(0, BLOCKSIZE):
        # Amplitude modulation:
        theta = theta + om
        output_block[n] = int( input_tuple[n] * math.cos(theta) )
    # keep theta betwen -pi and pi
    while theta > math.pi:
        theta = theta - 2 * math.pi

    X = np.fft.fft(input_tuple)
    Y = np.fft.fft(output_block)

    # Update y-data of plot
    if DBscale:
        line1.set_ydata(20 * np.log10(np.abs(X)))
        line2.set_ydata(20 * np.log10(np.abs(Y)))
    else:
        line1.set_ydata(np.abs(X))
        line2.set_ydata(np.abs(Y))
    plt.pause(0.001)
    # plt.draw()
    output_bytes = struct.pack('h' * BLOCKSIZE, *output_block)
    # Write binary data to audio output stream
    stream.write(output_bytes)

plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print('* Finished')
