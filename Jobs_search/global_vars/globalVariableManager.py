import threading

class GlobalVariableManager(threading.Thread):
    def __init__(self):
        super().__init__(name="ProgressVariable")
        self._global_variable = 0.0
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            # Your thread's logic here
            pass

    def stop(self):
        self._stop_event.set()

    def get_global_variable(self):
        with self._lock:
            return self._global_variable

    def set_global_variable(self, value):
        with self._lock:
            self._global_variable = value