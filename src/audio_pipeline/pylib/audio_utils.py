import numpy as np
import itertools


#Convert bytestream to float32 array (yes I know this is greasy)
def get_frame(aChunk):
    sound_chunk = np.frombuffer(aChunk, dtype=np.int16) #convert bytestream to a 16-bit array
    abs_max = np.abs(sound_chunk).max()
    sound_chunk = sound_chunk.astype('float32')
    if abs_max > 0:
        sound_chunk /= 32768.0
    sound_chunk = sound_chunk.squeeze()  #Depends on the use case; may be problematic in future
    return sound_chunk
    


def flatten_list(list_of_lists):
    return np.array(list(itertools.chain(*list_of_lists)), dtype=np.float32)