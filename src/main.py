from audio_pipeline import Source_Handler
from whisper_pipeline import Whisper_Handler
import whisper


#TODO: Integrate global kill signal for all threads

audio_source = Source_Handler()
whisper_model = whisper.load_model("tiny.en")
transcript = []

whisper_handler = Whisper_Handler(audio_source, whisper_model, transcript, threshold=0.10)


#TODO: Redo this section and put the thing in jupyter
if __name__ == "__main__":
    while True:
        try: 
            wordcount = whisper_handler.poll_model()    #Whole system should be fast enough that at most only one new word is captured since last poll
            if wordcount > 0:
                print(transcript[-wordcount:])

        except KeyboardInterrupt:
            break

    print("\n\nTranscript: " + str(transcript))
    whisper_handler.deactivate()