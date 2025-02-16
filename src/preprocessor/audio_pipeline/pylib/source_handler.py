#This module controls the ingoing audio feed.
#There are two possible source types: 1) Microphone Audio Stream, 2) Speaker Audio Stream

#TODO: Implement speaker audio stream and selection mechanism


import pyaudio


class Source_Handler:

    def __init__(self, format=pyaudio.paInt16, channels=1, sample_rate=16000, num_samples=512):
        self.format = format
        self.channels = channels
        self.sample_rate = sample_rate
        self.num_samples = num_samples
        self.chunk = int(sample_rate / 10)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.sample_rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)



    def get_chunk(self):
        self.audio_chunk = self.stream.read(self.num_samples)
        return self.audio_chunk
