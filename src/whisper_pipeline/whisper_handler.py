from audio_pipeline import Audio_Queue
from utils import flatten_list
from .listener import Listener
from audio_pipeline import Source_Handler
from vad_handler import VAD_Handler
import numpy as np
import torch
from faster_whisper import WhisperModel


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
        
        if count > 0:
            context = flatten_list(words)
            #result =  self.model.transcribe(np.array(context), fp16=torch.cuda.is_available())
            #self.transcript.append(result['text'].strip())
            
            segments, _ = self.model.transcribe(np.array(context, dtype=np.float32))
            for segment in segments:
                self.transcript.append(segment.text)
            

        return count

