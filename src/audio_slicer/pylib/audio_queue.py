import threading

class Audio_Queue:

    def __init__(self):
        self.length = 30
        self.index = 0
        self.lock = threading.Lock()
        self.queue = []
        

    def put(self, val: float):
        with self.lock:
            self.queue[self.index] = val
            self.index = (self.index + 1) % self.length


    #This may need to be reversed; might be better to bound on i < self.length
    def dump(self):
        with self.lock:
            ret = []
            i = self.index - self.length + 1
            j = 0
            while i < self.index:
                ret[j] = self.queue[i]
                i += 1
                j += 1
            return ret