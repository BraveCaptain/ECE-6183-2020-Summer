from struct import pack
from math import sin, pi
import wave

Fs = 8000

# Write a stereo wave file

wf = wave.open('lab1_8.wav', 'w')
wf.setnchannels(4)			# two channels (stereo)
wf.setsampwidth(2)			# two bytes per sample (16 bits per sample)
wf.setframerate(Fs)			# samples per second
A = 2**15 - 1.0 			# amplitude
f1 = 261.6				# frequency in Hz (middle C)
f2 = 440.0  				# note A4
f3 = 660.0				# some certain frequency
f4 = 880.0
N = int(0.5*Fs)				# half-second in samples

for n in range(0, N):		# half-second loop 

	# channel 1
	x = A * sin(2*pi*f1/Fs*n)
	byte_string = pack('h', int(x))
	# 'h' stands for 'short integer' (16 bits)
	wf.writeframes(byte_string)

	# channel 2
	x = A * sin(2*pi*f2/Fs*n)
	byte_string = pack('h', int(x))  # concatenation
	wf.writeframes(byte_string)
	
	#channel 3
	x = A * sin(2*pi*f3/Fs*n)
	byte_string = pack('h', int(x))  # concatenation
	wf.writeframes(byte_string)

	#channel 4
	x = A * sin(2*pi*f4/Fs*n)
	byte_string = pack('h', int(x))  # concatenation
	wf.writeframes(byte_string)

wf.close()
