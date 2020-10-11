# keyboard_demo_06.py
# Play a note using a second-order difference equation
# when the user presses a key on the keyboard.

import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk    

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 2      # Decay time (seconds)
f0 = 440    # Frequency (Hz)
freqs = [0] * 12
om = [0] * 12
a = [0,0,0] * 12
b = [0] * 12
# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
for i in range(12):
    freqs[i] = 2 ** (i/12) * f0
    om[i] = 2.0 * pi * float(freqs[i])/RATE
    a[i] = [1, -2*r*cos(om[i]), r**2]
    b[i] = [r*sin(om[i])]
    
# Filter coefficients (second-order IIR)
ORDER = 2   # filter order

states = [np.zeros(ORDER),np.zeros(ORDER),np.zeros(ORDER),np.zeros(ORDER),np.zeros(ORDER),np.zeros(ORDER),np.zeros(ORDER),np.zeros(ORDER),np.zeros(ORDER),np.zeros(ORDER),np.zeros(ORDER),np.zeros(ORDER)]

x = [np.zeros(BLOCKLEN), np.zeros(BLOCKLEN), np.zeros(BLOCKLEN), np.zeros(BLOCKLEN),np.zeros(BLOCKLEN), np.zeros(BLOCKLEN), np.zeros(BLOCKLEN), np.zeros(BLOCKLEN),np.zeros(BLOCKLEN), np.zeros(BLOCKLEN), np.zeros(BLOCKLEN), np.zeros(BLOCKLEN)]
y = [0] * 12
Y = np.zeros(BLOCKLEN)

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
        format      = PA_FORMAT,
        channels    = CHANNELS,
        rate        = RATE,
        input       = False,
        output      = True,
        frames_per_buffer = 128)
# specify low frames_per_buffer to reduce latency

CONTINUE = True
KEYPRESS = [False] * 12
def my_function(event):
    global CONTINUE
    global KEYPRESS
    print('You pressed ' + event.char)
    s = event.char
    if s == 'q':
        print('Good bye')
        CONTINUE = False
    elif s == '1':
        KEYPRESS[0] = True
    elif s == '2':
        KEYPRESS[1] = True
    elif s == '3':
        KEYPRESS[2] = True
    elif s == '4':
        KEYPRESS[3] = True
    elif s == '5':
        KEYPRESS[4] = True
    elif s == '6':
        KEYPRESS[5] = True
    elif s == '7':
        KEYPRESS[6] = True
    elif s == '8':
        KEYPRESS[7] = True
    elif s == '9':
        KEYPRESS[8] = True
    elif s == '0':
        KEYPRESS[9] = True
    elif s == '-':
        KEYPRESS[10] = True
    elif s == '=':
        KEYPRESS[11] = True
        

root = Tk.Tk()
root.bind("<Key>", my_function)

print('Press 1 2 3 4 5 6 7 8 9 0 - = for sound.')
print('Press "q" to quit')

while CONTINUE:
    root.update()
    for i in range (12):
        if KEYPRESS[i]:
            # Some key (not 'q') was pressed
            x[i][0] = 10000.0
    for i in range (12):
        [y[i], states[i]] = signal.lfilter(b[i], a[i], x[i], zi = states[i])
        x[i][0] = 0.0        
        KEYPRESS[i] = False
        y[i] = np.clip(y[i].astype(int), -MAXVALUE, MAXVALUE)     # Clipping      
        Y += y[i]
    binary_data = struct.pack('h' * BLOCKLEN, *(y[0] + y[1] + y[2] + y[3] + y[4] + y[5] + y[6] + y[7] + y[8] + y[9] + y[10] + y[11]));    # Convert to binary binary data
    stream.write(binary_data, BLOCKLEN)               # Write binary binary data to audio output

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()
