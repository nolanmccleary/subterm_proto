import numpy as np


class Frame_Handler: 
        
    def get_frame(self, aChunk):
        sound_chunk = np.frombuffer(aChunk(), np.int16) #convert bytestream to a 16-bit array
        abs_max = np.abs(sound_chunk).max()
        sound_chunk = sound_chunk.astype('float32')
        if abs_max > 0:
            sound_chunk *= 1/32768
        sound_chunk = sound_chunk.squeeze()  # depends on the use case
        return sound_chunk