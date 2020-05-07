import pyaudio
import numpy as np
import wave
import struct
import sys

CHUNK = 1024


class AudioPlayer:

    def __init__(self, filename):

        self.spf = wave.open(filename, 'rb')
        # File='../video_1.wav'
        self.signal = np.fromstring(self.spf.readframes(-1), 'Int16')
        self.p = pyaudio.PyAudio()
        self.ratio = len(self.signal)/self.spf.getnframes()
        self.stream = self.p.open(format=self. p.get_format_from_width(self.spf.getsampwidth()),
                                  channels=self.spf.getnchannels(),
                                  rate=self.spf.getframerate(),
                                  output=True)

    def play(self, start):
        start_idx = int(start*self.spf.getframerate()*self.ratio)
        signal = self.signal[start_idx:]
        sig=signal[1:CHUNK]

        inc = 0
        data=0

        #play
        while data != '':
            data = struct.pack("%dh"%(len(sig)), *list(sig))
            self.stream.write(data)
            inc=inc+CHUNK
            sig=signal[inc:inc+CHUNK]

    def terminate(self):
        self.stream.close()
        self.p.terminate()


filename = sys.argv[1]
start_time = int(sys.argv[2])
audio_player = AudioPlayer(filename)
audio_player.play(start_time)