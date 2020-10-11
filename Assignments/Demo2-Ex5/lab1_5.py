# lab1_5


from struct import pack
from math import sin, pi
import wave

Fs = 10000

# Write a mono wave file 

wf = wave.open('lab1_5.wav', 'w')	# wf : wave file
wf.setnchannels(1)			# one channel (mono)
wf.setsampwidth(1)			# 1 byte per sample (8 bits per sample)
wf.setframerate(Fs)			# samples per second
A = 2**7 - 1.0 				# amplitude
f = 220.0				

for n in range(0, int(0.5*Fs)):
	x = A * sin(2*pi*f/Fs*n)
	#'B' stands for unsigned char
	byte_string = pack('B', int(x+128)) 
	wf.writeframesraw(byte_string)
wf.close()
