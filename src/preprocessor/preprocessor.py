from audio_pipeline.pylib import Source_Handler
from audio_slicer.pylib import Frame_Handler
from model_handler.pylib import Model_Handler


class Preprocessor:

    def __init__(self, source: Source_Handler):
        self.source = source
        self.frame_handler = Frame_Handler()
        self.model_handler = Model_Handler()


    def process_chunk(self):
        return self.model_handler.get_confidence(self.frame_handler.get_frame(self.source.get_chunk()))