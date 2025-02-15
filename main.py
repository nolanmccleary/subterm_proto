#! python3.7
from sys import platform

from pylib import Transcription_Handler
from pylib import Audio_Handler


gAudio = Audio_Handler()
gTranscript = Transcription_Handler(gAudio)


def main():
    print("Begin audio capture")
    while True:
        try:
            print(gAudio.data_queue.qsize())
            gTranscript.process_audio()
            gAudio.data_queue.qsize()
            #gTranscript.print_transcript_latest()
    
        except KeyboardInterrupt:
            print("\n\nFull Transcript:")
            gTranscript.print_full_transcript()
            break



if __name__ == "__main__":
    print("PLATFORM: " + str(platform))
    main()