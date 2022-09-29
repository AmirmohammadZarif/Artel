# import pyaudio
# import wave
# import sys
# p = pyaudio.PyAudio()
# CHUNK = 1024
# wf = wave.open('/Users/theamircoder/Desktop/file.wav', 'rb')
# # open stream (2)
# stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                 channels=wf.getnchannels(),
#                 rate=wf.getframerate(),
#                 output=True)
# data = wf.readframes(CHUNK)


# # play stream (3)
# while len(data) > 0:
#     stream.write(data)
    
#     data = wf.readframes(CHUNK)
#     print(wf)

# # stop stream (4)
# stream.stop_stream()
# stream.close()



import pyaudio
import numpy as np
import wave
import sys
import time
p = pyaudio.PyAudio()
CHUNK = 1024
wf = wave.open('/Users/theamircoder/Desktop/file.wav', 'rb')
# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)


RATE = 44100

stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)

# stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                 channels=wf.getnchannels(),
#                 rate=wf.getframerate(),
#                 output=True)
data = wf.readframes(CHUNK)
for i in range(int(120*wf.getframerate()/1024)): #go for a few seconds
    
    data = wf.readframes(CHUNK)
    stream.write(data)
    data = np.fromstring(wf.readframes(CHUNK),dtype=np.int16)
    # peak=np.average(np.abs(data))*2
    bars="#"*int(50*peak/2**16)
    print("%04d %05d %s"%(i,peak,bars))
    time.sleep(0.026)

stream.stop_stream()
stream.close()
p.terminate()
