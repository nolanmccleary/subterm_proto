from .audio_queue import Audio_Queue, flatten_list
from .listener import Listener
from audio_pipeline import Source_Handler
import threading
import torch
from whisper import Whisper


"""
@Brief: This is how we do - 

1) Keep context window full of last n wordly sounds (sounds most likely coming from speech) and feed through model whenver we detect a word has ended (we can have a full context window without a performance drop because transformer models are inherently parallelizeable and everything is running on a GPU).
We want a full context buffer because the model is most accurate this way.

2) We then take the model output and add it to our transcript.

Keep in mind 'word' here is used very loosely and it's more like a discrete unit of voice data that can be converted to an attention vector
"""

#The idea is to pass this thing a source and a whisper model and it generates a transcript
class Whisper_Handler:

    def __init__(self, source: Source_Handler, model: Whisper, transcript):
        self.source = source
        self.model = model
        self.audio_data = Audio_Queue()
        self.listener = Listener(self.source, self.audio_data)  #Listener thread starts in background here
        self.transcript = transcript
        self.context = []
        self.continue_transcription = False



    def poll_model(self):
        (words, count) = self.audio_data.dump()
        while count > 0:
            context = flatten_list(words[0 : -1 * count])
            result =  self.model.transcribe(context, fp16=torch.cuda.is_available())
            self.transcript.append(result)
            count -= 1



    def transcribe_audio(self):
        self.continue_transcription = True
        while self.continue_transcription:
            self.poll_model()
            print(self.transcript[-1])



    def activate(self):
        thread2 = self.listener.start_audio_capture()
        thread1 = threading.Thread(target=self.transcribe_audio)
        thread1.start
        return (thread1, thread2)



    def deactivate(self):
        self.listener.stop_audio_capture()