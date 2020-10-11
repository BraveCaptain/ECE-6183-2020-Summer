import pyaudio, wave, struct, math
import numpy as np
import scipy.signal
from myfunctions import bandpass_filter

# inilialize the output stream parameters
channels = 1
rate = 16000
width = 2

# set the output wave file parameters
output_wavfile = 'ans.wav'
output_wf = wave.open(output_wavfile, 'w')      # wave file
output_wf.setframerate(rate)
output_wf.setsampwidth(width)
output_wf.setnchannels(channels)

p = pyaudio.PyAudio()
# Open audio stream
stream = p.open (
    format      = p.get_format_from_width(width),
    channels    = channels,
    rate        = rate,
    input       = False,
    output      = True )

# set block length
BLOCKLEN = 32
# inilialize state, with order 2 band pass filter
states = np.zeros(4)

# write to stream and file
for i in range (2048):
    
    # generate while noise with 500 average, 1000 standard deviation, size of 32
    whiteWave = np.random.normal(500, 1000, size=BLOCKLEN)
    
    # generate the center frequency 
    centerFreq = 2500 * (math.cos(0.005 * math.pi * i) + 2)
    
    # apply the bandpass filter
    [output, states] = bandpass_filter(whiteWave, centerFreq, rate, states)
    # enlarge the amplitude of the output wave
    for j in range(BLOCKLEN):
        output[j] *= 26
    # generate the binary data
    binary_data = struct.pack('h' * BLOCKLEN, *output)
    # write to wave file
    output_wf.writeframes(binary_data)
    # write to stream
    stream.write(binary_data)

stream.stop_stream()
stream.close()
p.terminate()

output_wf.close()
