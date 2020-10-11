from math import cos, pi 
import pyaudio, struct
import tkinter as Tk
import pyaudio, wave, struct, math
import numpy as np
import scipy.signal
from myfunctions import bandpass_filter   	

# quit function
def fun_quit():
  global CONTINUE
  print('Good bye')
  CONTINUE = False


Fs = 16000     # rate (samples/second)

# Define Tkinter root
root = Tk.Tk()

# Define Tk variables
changeRate = Tk.DoubleVar()
bandWidth = Tk.DoubleVar()

# Initialize Tk variables
changeRate.set(1)
bandWidth.set(100)

# Define widgets
S_rate = Tk.Scale(root, label = 'Changing rate', variable = changeRate, from_ = 1, to = 10)
S_bandWidth = Tk.Scale(root, label = 'Bandwidth', variable = bandWidth, from_ = 100, to = 500)
B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)

# Place widgets
B_quit.pack(side = Tk.BOTTOM, fill = Tk.X)
S_rate.pack(side = Tk.LEFT)
S_bandWidth.pack(side = Tk.LEFT)

# Create Pyaudio object
p = pyaudio.PyAudio()
stream = p.open(
  format = pyaudio.paInt16,  
  channels = 1, 
  rate = Fs,
  input = False, 
  output = True,
  frames_per_buffer = 32)
  # specify low frames_per_buffer to reduce latency

BLOCKLEN = 32
output_block = [0] * BLOCKLEN
states = np.zeros(4)
CONTINUE = True
i = 0

print('* Start')
while CONTINUE:
  
  root.update()
  # generate white noise
  whiteWave = np.random.normal(500, 1000, size=BLOCKLEN)
  # generate center frequency
  centerFreq = 1000 * (math.cos(changeRate.get() / 2000 * math.pi * i) + 2)
  # bandpass filter
  [output_block, states] = bandpass_filter(whiteWave, centerFreq, Fs, states, bandWidth.get())
  # enlarge amplitude
  for j in range(BLOCKLEN):
    output_block[j] *= 3
  # generate binary data
  binary_data = struct.pack('h' * BLOCKLEN, *output_block)   # 'h' for 16 bits
  stream.write(binary_data)
  i += 1

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
