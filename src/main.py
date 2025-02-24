import argparse
from audio_pipeline import Source_Handler
from whisper_pipeline import Whisper_Handler
from utils import stop_flag as stop
from faster_whisper import WhisperModel





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="tiny", help="Model to use")
    #parser.add_argument("--translate_enabled", action='store_true', default=".en", help="Model to use")

    args = parser.parse_args()

    #if args.translate_enabled:
    #    model_name = args.model 
    #else:
        #model_name = args.model + ".en"  #Yes I know this is bizarre and stupid, I'll fix later


    audio_source = Source_Handler()
    whisper_model = WhisperModel(model_size_or_path=args.model, device="cpu") #TODO: Device should be based on available system specs
    
    transcript = []

    whisper_handler = Whisper_Handler(audio_source, whisper_model, transcript, threshold=0.09)

    while not stop.get_status():
        try: 
            wordcount = whisper_handler.poll_model()    #Whole system should be fast enough that at most only one new word is captured since last poll
            if wordcount > 0:
                print(transcript[-wordcount:][0])

        except KeyboardInterrupt:
            #whisper_handler.deactivate()
            stop.update_status(True)
            break

    print("\n\nTranscript: " + str(transcript))