import argparse
from audio_pipeline import Source_Handler
from whisper_pipeline import Whisper_Handler
import whisper


#TODO: Integrate global kill signal for all threads


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="tiny", help="Model to use")
    parser.add_argument("--translate_enabled", type=str, default=".en", help="Model to use")

    args = parser.parse_args()

    if args.translate_enabled == "ON":
        model_name = args.model 
    else:
        model_name = args.model + args.translate_enabled    #Yes I know this is bizarre and stupid, I'll fix later


    audio_source = Source_Handler()
    whisper_model = whisper.load_model(model_name)
    transcript = []
    whisper_handler = Whisper_Handler(audio_source, whisper_model, transcript, threshold=0.09)

    while True:
        try: 
            wordcount = whisper_handler.poll_model()    #Whole system should be fast enough that at most only one new word is captured since last poll
            if wordcount > 0:
                print(transcript[-wordcount:][0])

        except KeyboardInterrupt:
            break

    print("\n\nTranscript: " + str(transcript))
    whisper_handler.deactivate()