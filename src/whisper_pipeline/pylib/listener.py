from audio_pipeline import Source_Handler
from .audio_queue import Audio_Queue, flatten_list
from preprocessor import Preprocessor
import threading


class Listener:

    def __init__(self, source: Source_Handler, audio_data: Audio_Queue, sensitivity=0.5):
        self.source = source
        self.audio_data = audio_data
        self.sensitivity = sensitivity
        self.words_captured = 0
        self.source = Source_Handler()
        self.preprocessor = Preprocessor(self.source)
        self.continue_capture = False
        #self.start_audio_capture()


    def capture_audio(self):
        self.continue_capture = True
        prev_confidence_ceiling = 0
        word_buffer = []

        while self.continue_capture:

            (frame, confidence) = self.preprocessor.get_confidence()
            confidence_ceiling = self.sensitivity_ceiling(confidence)
            if prev_confidence_ceiling and not confidence_ceiling: #Word has finished, put in word buffer
                self.audio_data.put(word_buffer)

            elif confidence_ceiling: #Start or middle of word, in any case capture data
                word_buffer = flatten_list([word_buffer, frame]) #TODO: Make this not stupid

            else:   #Dead zone, wait for next word
                word_buffer = []

            prev_confidence_ceiling = confidence_ceiling



    def sensitivity_ceiling(self, confidence):
        return True if confidence > self.sensitivity else False



    def start_audio_capture(self):
        thread = threading.Thread(target=self.capture_audio)
        thread.start()
        return thread
    


    #Call upon program termination
    def stop_audio_capture(self):
        self.capture_audio = False

    

