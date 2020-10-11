
import wave

# help(wave)

# web page: https://docs.python.org/3/library/wave.html

wf = wave.open('lab1.wav')

print("number of channels: ", wf.getnchannels()) 	# number of channels

print("frame rate: " ,wf.getframerate()) 	# frame rate (number of frames per second)

print("total number of frames: ", wf.getnframes()) 		# total number of frames (length of signal)

print("number of bytes per sample: ", wf.getsampwidth()) 	# number of bytes per sample

wf.close()

##width is 2
