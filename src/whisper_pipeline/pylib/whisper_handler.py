from audio_pipeline import Audio_Queue
from utils import flatten_list
from .listener import Listener
from audio_pipeline import Source_Handler
from vad_handler import VAD_Handler
import numpy as np
import torch
from faster_whisper import WhisperModel

"""
@Brief: This is how we do - 

1) Keep context window full of last n wordly sounds (sounds most likely coming from speech) and feed through model whenver we detect a word has ended (we can have a full context window without a performance drop because transformer models are inherently parallelizeable and everything is running on a GPU).
We want a full context buffer because the model is most accurate this way.

^ So this is completely wrong and I'm an idiot. Compute time grows quadratically with context size because every attention vector influences every other attention vector.
I could delete this and squash the commit so I don't incriminate myself but writing this is more fun because its like a time capsule for roasts
-> Anyways, a context clamp should be added.

2) We then take the model output and add it to our transcript.

Keep in mind 'word' here is used very loosely and it's more like a discrete unit of voice data
"""




class Whisper_Handler:

    def __init__(self, source: Source_Handler, model: WhisperModel, transcript, threshold = 0.15):
        self.source = source
        self.vad = VAD_Handler()
        self.model = model
        self.audio_data = Audio_Queue()
        self.threshold = threshold
        self.listener = Listener(self.source, self.vad, self.audio_data, self.threshold)  #Listener thread starts in background here
        self.transcript = transcript
        self.context = []


    def poll_model(self):
        (words, count) = self.audio_data.dump()
        cpy = count
        
        while count > 0:
            context = flatten_list(words)
            result =  self.model.transcribe(np.array(context), fp16=torch.cuda.is_available())
            self.transcript.append(result['text'].strip())
            count -= 1
        return cpy


    def poll_model_last_word(self):
        context = flatten_list(self.audio_data.dump()[0])
        result = self.model.transcribe(np.array(context), fp16=torch.cuda.is_available())
        return result['text'].strip()


    def deactivate(self):
        self.listener.stop_audio_capture()