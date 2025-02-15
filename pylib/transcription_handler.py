import whisper
import torch
from .audio_handler import Audio_Handler

class Transcription_Handler:

    def __init__(self, audio_handler: Audio_Handler, model:str="tiny", mode:str=".en"):
        self.model = whisper.load_model(model + mode)
        self.audio_handler = audio_handler
        self.transcript = ['']
        print("Transcription handler initialized")


    def process_audio(self):
        if self.audio_handler.set_buffer():
            model_output = self.model.transcribe(self.audio_handler.audio_buffer, fp16=torch.cuda.is_available())['text'].strip() #Want to use fp16 if possible for greater speed
            if self.audio_handler.phrase_complete:
                self.transcript.append(model_output)
            else:
                self.transcript[-1] = model_output

    
    def print_transcript_latest(self):
        print(self.transcript[-1])


    def print_full_transcript(self):
        for line in self.transcript:
            print(line)