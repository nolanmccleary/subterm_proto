from audio_pipeline.pylib import Source_Handler
from audio_slicer.pylib import Frame_Handler
from vad_handler.pylib import VAD_Handler


class Preprocessor:

    def __init__(self, source: Source_Handler):
        self.source = source
        self.frame_handler = Frame_Handler()
        self.model_handler = VAD_Handler()


    def process_chunk(self):
        frame = self.frame_handler.get_frame(self.source.get_chunk())
        return (frame, self.model_handler.get_confidence(frame))
    





