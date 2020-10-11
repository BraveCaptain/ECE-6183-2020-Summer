import pyaudio
import wave
import struct

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return (x)

def playWaveFile(waveFile):
    wf = wave.open(waveFile)
    p = pyaudio.PyAudio()
    stream = p.open(
        format = pyaudio.paInt16,
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        input = False,
        output = True
    )
    input_bytes = wf.readframes(1)
    while len(input_bytes) > 0:
        input_tuple = struct.unpack('h', input_bytes)
        output_value = int(clip16(input_tuple[0]))
        output_bytes = struct.pack('h', output_value)
        stream.write(output_bytes)
        input_bytes = wf.readframes(1)
    stream.stop_stream()
    stream.close()
    p.terminate()
    

