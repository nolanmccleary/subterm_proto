from audio_pipeline.pylib import Source_Handler
import numpy as np



class Frame_Handler: 

    def __init__(self): 
        self.source = Source_Handler()
        self.source.initialize_stream()
        

    def get_frame(self):
        sound_chunk = np.frombuffer(self.source.get_chunk(), np.int16) #convert bytestream to a 16-bit array
        abs_max = np.abs(sound_chunk).max()
        sound_chunk = sound_chunk.astype('float32')
        if abs_max > 0:
            sound_chunk *= 1/32768
        sound_chunk = sound_chunk.squeeze()  # depends on the use case
        return sound_chunk