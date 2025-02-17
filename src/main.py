from preprocessor import Preprocessor
from audio_pipeline import Source_Handler
from audio_slicer import Audio_Queue
import whisper
import torch


#TODO: Find out how to get whisper model context length

audio_source = Source_Handler()
audio_preprocessor = Preprocessor(audio_source)
audio_queue = Audio_Queue()
whisper_model = whisper.load_model("tiny.en")


continue_recording = True
transcript = ['']




'''
#TODO: If this works well, do it in CUDA
FILTER_LEN = 3
filter = [0.0, 0.0, 0.0]
filter_weights = [0.165, 0.165, 0.67]
def update_filter(val:float):
    for i in range(1, FILTER_LEN-1):
        filter[i-1] = filter_weights[i-1] * filter[i]
    filter[FILTER_LEN-1] = filter_weights[FILTER_LEN-1] * val
    filter_avg = 0
    for i in range(0, FILTER_LEN-1):
        filter_avg += filter[i] * filter_weights[i]
    return filter_avg


#TODO: Redo this section and put the thing in jupyter
if __name__ == "__main__":
    word_start = False
    word_end = False
    result = []
    while True:
        try:
            (audio_frame, audio_confidence) = audio_preprocessor.process_chunk()
            audio_confidence = update_filter(audio_confidence)
            result = result
            if audio_confidence > 0.5:
                for val in audio_frame: #WILL PROBABLY NEED TO READJUST QUEUE SIZE
                    audio_queue.put(val)
                result = whisper_model.transcribe(audio_queue.dump(), fp16=torch.cuda.is_available())
                word_start = True
                word_end = False
            else:
                word_end = True if word_start else False
                word_start = False

            
            if word_end:
                transcript.append(result)

        except KeyboardInterrupt:
            break

    for line in transcript:
        print(line)

'''


    