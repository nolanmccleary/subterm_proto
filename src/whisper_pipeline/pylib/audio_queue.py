import threading
from typing import List
import itertools


#Ihis is all highly sub-optimal; static buffers should be used for anything production-worthy
class Audio_Queue:

    def __init__(self, maxlen=30):
        self.length = maxlen
        self.index = 0
        self.lock = threading.Lock()
        self.queue = [0 * self.length]
        self.count = 0


    def put(self, val: List[float]) -> None:
        with self.lock:
            self.queue[self.index] = val
            self.index = (self.index + 1) % self.length
            self.count += 1


    #This may need to be reversed; might be better to bind it on i < self.length
    def dump(self) -> List[List[float]]:
        with self.lock:
            ret = []
            i = (self.index + 1) % self.length

            while i != self.index:
                ret.append(self.queue[i])
                i = (i + 1) % self.length

            count = self.count
            self.count = 0
            return (ret, count) #returns an array of the last <length> words as well as the number of new words added since the last dump
        



def flatten_list(list_of_lists):
    return list(itertools.chain(*list_of_lists))