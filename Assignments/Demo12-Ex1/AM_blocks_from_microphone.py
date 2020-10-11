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
from matplotlib import pyplot

# f0 = 0      # Normal audio
f0 = 400    # Modulation frequency (Hz)

BLOCKLEN = 1024      # Number of frames per block
WIDTH = 2           # Number of bytes per signal value
CHANNELS = 1        # mono
RATE = 32000        # Frame rate (frames/second)
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)


output_block = BLOCKLEN * [0]

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
# Initialize phase
om = 2*math.pi*f0/RATE
theta = 0

# Number of blocks to run for
num_blocks = int(RATE / BLOCKLEN * RECORD_SECONDS)

print('* Recording for %.3f seconds' % RECORD_SECONDS)

# Start loop
for i in range(0, num_blocks):

    # Get frames from audio input stream
    # input_bytes = stream.read(BLOCKLEN)       # BLOCKLEN = number of frames read
    input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)   # BLOCKLEN = number of frames read

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)
   
    # Go through block
    for n in range(0, BLOCKLEN):
        # No processing:
        # output_block[n] = input_tuple[n]  
        # OR
        # Amplitude modulation:
        theta = theta + om
        output_block[n] = int( input_tuple[n] * math.cos(theta) )


    # keep theta betwen -pi and pi
    while theta > math.pi:
        theta = theta - 2 * math.pi

    
    g1.set_ydata(input_tuple)   # Update y-data of plot
    g2.set_ydata(output_block)   # Update y-data of plot
    pyplot.pause(0.00001)
    
    # Convert values to binary data
    output_bytes = struct.pack('h' * BLOCKLEN, *output_block)
    # Write binary data to audio output stream
    stream.write(output_bytes)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
