from preprocessor import Preprocessor
from audio_pipeline import Source_Handler

import threading


source = Source_Handler()
preprocessor = Preprocessor(source)




if __name__ == "__main__":
    print("Begin")