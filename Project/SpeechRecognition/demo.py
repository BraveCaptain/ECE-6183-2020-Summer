import pyaudio
import tkinter as Tk
import numpy as np
import struct
import math
from tkinter import filedialog
from SpeechRecognition import SpeechRecognition
from os import path
import helper
import _thread
import wave

def realTimeWaveFile():
    BLOCKLEN = 30000
    default_dir = "/Users/QY_Tang/Dropbox/NYU/DSP Lab/project/english.wav"
    filePath = Tk.filedialog.askopenfilename(title='File Selection', initialdir=(path.expanduser(default_dir)))
    if filePath == '':
        return
    _thread.start_new_thread(helper.playWaveFile, (filePath, ))
    
    wf = wave.open( filePath, 'rb')
    LEN = wf.getnframes() 
    audioData = np.asarray(np.int16([]))
    num_blocks = int(math.floor(LEN  / BLOCKLEN))
    res = ""
    for i in range(0, num_blocks):
        input_bytes = wf.readframes(BLOCKLEN)
        input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)
        audioSeg = np.asarray(np.int16(input_tuple))
        audioData = np.concatenate((audioData, audioSeg), axis=0)
        sr.getStringFromBin(audioData, wf.getframerate(), wf.getsampwidth())
    res = sr.getStringFromBin(audioData, wf.getframerate(), wf.getsampwidth())
    text.delete(1.0, Tk.END)
    text.insert(1.0, res)
    wf.close()

def realTimeMicrophone():
    BLOCKLEN = 15000
    WIDTH       = 2         # Number of bytes per sample
    CHANNELS    = 1         # mono
    RATE        = 16000     # Sampling rate (frames/second)
    DURATION    = 6         # duration of processing (seconds)
    N = int(DURATION * RATE / BLOCKLEN)     # N : Number of samples to process
    
    p = pyaudio.PyAudio()

    stream = p.open(
        format      = p.get_format_from_width(WIDTH),
        channels    = CHANNELS,
        rate        = RATE,
        input       = True,
        output      = False)
    audioData = np.asarray(np.int16([]))
    print("Please speak now!")
    for n in range(0, N):
        input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)
        input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)
        audioSeg = np.asarray(np.int16(input_tuple))
        audioData = np.concatenate((audioData, audioSeg), axis=0)
        _thread.start_new_thread(sr.getStringFromBin, (audioData, RATE, WIDTH,))
    res = sr.getStringFromBin(audioData, RATE, WIDTH)
    text.delete(1.0, Tk.END)
    text.insert(1.0, res)
    p.terminate()

def fileSelect():
    default_dir = "/Users/QY_Tang/Dropbox/NYU/DSP Lab/project/author.wav"
    filePath = Tk.filedialog.askopenfilename(title='File Selection', initialdir=(path.expanduser(default_dir)))
    if filePath == '':
        return
    _thread.start_new_thread(helper.playWaveFile, (filePath, ))
    res = sr.getStringFromFile(filePath)
    text.delete(1.0, Tk.END)
    text.insert(1.0, res)


def microphoneRecognize():
    res = sr.getStringFromMicrophone()
    text.delete(1.0, Tk.END)
    text.insert(1.0, res)

root = Tk.Tk()
sr = SpeechRecognition()

textVar = Tk.StringVar()
textVar.set("CMU Sphinx Speech Recognition Demo")

textLabel = Tk.Label(root, textvariable = textVar)
textLabel.pack()

text = Tk.Text(root, width=50, height=10, yscrollcommand = True)
text.insert(1.0, "Your speech will output here...")
text.pack()

fileBtn = Tk.Button(root, text = 'Select wave file', command = fileSelect)
fileBtn.pack()

realTimeFileBtn = Tk.Button(root, text = 'Real-time wave file recognition', command = realTimeWaveFile)
realTimeFileBtn.pack()

microphoneBtn = Tk.Button(root, text = 'Record your speech', command = microphoneRecognize)
microphoneBtn.pack()

realTimeMicrophoneBtn = Tk.Button(root, text = 'Real-time speech recognition', command = realTimeMicrophone)
realTimeMicrophoneBtn.pack()

root.mainloop()

