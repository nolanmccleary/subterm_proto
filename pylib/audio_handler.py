#! python3.7
import numpy as np
import speech_recognition as sr
import threading

from datetime import datetime, timedelta, timezone
from collections import deque
from sys import platform



class Audio_Handler:

###################################### INITIALIZATION BLOCK #########################################################################

    def __init__(self, energy_threshold=1000, record_timeout=2, phrase_timeout=3, sample_rate=16000, microphone='pipewire'):
        self.energy_threshold = energy_threshold
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout
        self.sample_rate = sample_rate
        self.microphone = microphone
        
        self.platform = platform
        
        self.mic_index = -1
        self.source = None

        self.data_queue = ThreadSafeDeque(maxlen=3) #TODO: Figure out appropriate sizing
        self.recorder = sr.Recognizer()

        self.phrase_complete = False
        self.audio_buffer = None

        self.initialize()
        self.time = datetime.now(timezone.utc)
        print("Audio handler Initialized")



    def initialize(self):
        self.initialize_source()
        self.initialize_recorder()



    def initialize_source(self):
        self.get_mic_index()
        if self.mic_index == -1:
            print("Error! Cannot get mic index")
        self.source = sr.Microphone(sample_rate=self.sample_rate, device_index=self.mic_index)



    def initialize_recorder(self):
        self.recorder.energy_threshold = self.energy_threshold
        self.recorder.dynamic_energy_threshold = False
        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)
        self.recorder.listen_in_background(self.source, self.record_callback, phrase_time_limit=self.record_timeout) #Create background listener thread



############################################## RUNTIME BLOCK ##########################################################################
    #TODO: Investigate fsm-based audio slicing
    def set_buffer(self):
        now = datetime.now(timezone.utc)
        #Check 1: We have audio data
        #Check 2: Our phrase is complete
        if self.data_queue: 
            if now - self.time > timedelta(seconds=self.phrase_timeout):
                self.phrase_complete = True
                self.time = now

            else: 
                self.phrase_complete = False
            print("DATA QUEUE: " + str(self.data_queue))
            self.audio_buffer = np.frombuffer(b''.join(self.data_queue), dtype=np.int16).astype(np.float32) / 32768.0
            return True
        return False

################################## AUXILLARY FUNCTIONS ############################################################################
    def get_mic_index(self):
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(index)
            if self.microphone in name:
                print("CHOSEN MIC NAME: " + str(name) + "CHOSEN MIC_INDEX: " + str(index))
                self.mic_index = index
                break
        return 



    def record_callback(self, _, audio: sr.AudioData) -> None:
        print("callback")
        data = audio.get_raw_data()
        self.data_queue.append(data)
        



    def print_devices(self):
        print("Available microphone devices are: ")
        for _, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"Microphone with name \"{name}\" found")
        return
    


    def device_check(self):
        print("..................................Audio Settings........................\n" + "SOURCE: " + str(self.source) + "RECORDER: " + str(self.recorder) + "\n.......................................................................")




######################################### Deque isn't thread-safe by default ####################################################

#TODO: Make this true circular
class ThreadSafeDeque:
    def __init__(self, maxlen=None):
        self.deque = deque(maxlen=maxlen)
        self.lock = threading.Lock()

    def append(self, item):
        with self.lock:
            self.deque.append(item)

    def appendleft(self, item):
        with self.lock:
            self.deque.appendleft(item)

    def pop(self):
        with self.lock:
            return self.deque.pop()

    def popleft(self):
        with self.lock:
            return self.deque.popleft()

    def __getitem__(self, index):
        with self.lock:
            return self.deque[index]

    def __len__(self):
        with self.lock:
            return len(self.deque)

    def clear(self):
        with self.lock:
            self.deque.clear()