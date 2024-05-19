import threading
import time

class GlobalVariable:
    def __init__(self):
        self._value = 0.0
        self._lock = threading.Lock()

    def set_value(self, value):
        with self._lock:
            self._value = value
            

    def get_value(self):    
        with self._lock:
            return self._value
        
    # Implement __reduce__ method for serialization
    def __reduce__(self):
        # We return a tuple with the class constructor and its arguments
        return (self.__class__, ())