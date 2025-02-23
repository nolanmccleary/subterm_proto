import os
import torch

#TODO: Change this to VAD_Handler; add top-level whisper/VAD handler
class VAD_Handler:
    
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model/JIT/silero_vad.jit')

        torch.set_num_threads(1)
        torch.set_grad_enabled(False)
        torch._C._jit_set_profiling_mode(False)
        self.device = torch.device('cpu')   #TODO: Move these global torch configs to a top-level model handler
        self.model = torch.jit.load(self.model_path, map_location=self.device)
        
         

    #Gets confidence that given audio chunk contains voice data
    def get_confidence(self, audio_float32):
        return (audio_float32, self.model(torch.from_numpy(audio_float32), 16000).item())