import torch

#TODO: Change this to VAD_Handler; add top-level whisper/VAD handler
class Model_Handler:
    
    def __init__(self):
        self.model, self.utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True)
        (self.get_speech_timestamps,
         self.save_audio,
         self.read_audio,
         self.VADIterator,
         self.collect_chunks) = self.utils
        

    #Gets confidence that given audio chunk contains voice data
    def get_confidence(self, audio_float32):
        return self.model(torch.from_numpy(audio_float32), 16000).item()