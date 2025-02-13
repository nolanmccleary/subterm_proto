#! python3.7
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform


#TODO: Add whisper.cpp; add multibuffering


def main():

    model = "tiny.en"
    audio_model = whisper.load_model(model)

    mic_name = 'pipewire'
    record_timeout = 2
    phrase_timeout = 3

    print("CAPABILITY:" + str(torch.cuda.get_device_capability()))
    print("FP16: " + str(torch.cuda.is_available()))

    index = 0
    for _, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone with name \"{name}\" found")
        if mic_name in name:
            break
        index += 1
    
    #source = sr.Microphone(sample_rate=16000, device_index=index)
    source = sr.Microphone(sample_rate=16000)

    phrase_time = None
    data_queue = Queue()
    recorder = sr.Recognizer()
    recorder.energy_threshold = 1000
    recorder.dynamic_energy_threshold = False


    with source:
        recorder.adjust_for_ambient_noise(source)


    def record_callback(_, audio:sr.AudioData) -> None:
        data = audio.get_raw_data()
        data_queue.put(data)

    #Create background listening thread
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)
    
    transcript = ['']
    print("Begin transcription...")


    while True:
        try:
            now = datetime.now()
            if not data_queue.empty():
                phrase_complete = False
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    phrase_complete = True

                phrase_time = now
                
                # create buffer and clear queue
                audio_data = b''.join(data_queue.queue)
                data_queue.queue.clear()
                
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                if phrase_complete:
                    transcript.append(text)
                else:
                    transcript[-1] = text

                # Clear the console to reprint the updated transcription avia flushing stdout (faster that way)
                os.system('cls' if os.name=='nt' else 'clear')
                for line in transcript:
                    print(line)
                print('', end='', flush=True)
            
            else:
                sleep(0.25)
        
        except KeyboardInterrupt:
            break

    print("\n\nTranscription:")
    for line in transcript:
        print(line)











if __name__ == "__main__":
    main()
