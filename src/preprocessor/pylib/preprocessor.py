from audio_pipeline.pylib import Source_Handler
from audio_slicer.pylib import Frame_Handler
from vad_handler.pylib import VAD_Handler

#TODO: Get rid of this
class Preprocessor:

    def __init__(self, source: Source_Handler, filter_weights=[0.165, 0.165, 0.67]):
        self.source = source
        self.frame_handler = Frame_Handler()
        self.model_handler = VAD_Handler()
        self.filter_weights = filter_weights
        self.filter_len = len(self.filter_weights)
        self.filter = [0 for _ in range(self.filter_len)]
        self.unfiltered_confidence = 0        



    def get_confidence(self):
        frame = self.frame_handler.get_frame(self.source.get_chunk())
        return (frame, self.model_handler.get_confidence(frame))



    #So far filtering seems useless
    def get_filtered_confidence(self):
        frame = self.frame_handler.get_frame(self.source.get_chunk())
        confidence = self.model_handler.get_confidence(frame)
        self.unfiltered_confidence = confidence

        for i in range(1, self.filter_len-1):
            self.filter[i-1] = self.filter_weights[i-1] * self.filter[i]
        self.filter[self.filter_len-1] = self.filter_weights[self.filter_len-1] * confidence
        filtered_confidence = 0
        
        for i in range(self.filter_len):
            filtered_confidence += self.filter[i] * self.filter_weights[i]
        
        return (frame, filtered_confidence)