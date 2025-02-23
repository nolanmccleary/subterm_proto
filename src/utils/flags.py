import threading


class Flag:

    def __init__(self, start_status=False):
        self.status = start_status
        self.lock = threading.Lock()

    def update_status(self, new_status):
        with self.lock:
            self.status = new_status

    def get_status(self):
        with self.lock:
            return self.status
        

stop_flag = Flag()