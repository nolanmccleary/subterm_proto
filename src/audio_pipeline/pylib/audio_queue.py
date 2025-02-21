import threading


#Ihis is all highly sub-optimal; static buffers should be used for anything production-worthy
class Audio_Queue:

    def __init__(self, maxlen=30):
        self.length = maxlen
        self.index = 0
        self.lock = threading.Lock()
        self.queue = [[0.0] for _ in range(self.length)]
        self.count = 0


    def put(self, val) -> None:
        with self.lock:
            self.queue[self.index] = val
            self.index = (self.index + 1) % self.length
            self.count = min(self.count + 1, self.length)
            #print("PUSH" + str(val))


    #Spit out the n <= lengthnewest words added into the queue since last dump
    def dump(self):
        with self.lock:
            ret = []
            count = self.count
            if count > 0:
                ret = [[0] for _ in range(self.count)]
                i = self.index - self.count
                j = 0
            
                while i != self.index:
                    ret[j] = self.queue[i]
                    i = (i + 1) % self.length
                    j += 1
                
                #print("PULL" + str(ret))
                #print(self.count)
                self.count = 0

            return (ret, count) #returns an array of the last <length> words as well as the number of new words added since the last dump
        
