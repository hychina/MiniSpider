import threading

def get_thread_name(fn):
    def wrapper(self, *args, **kwargs):
        self.name = threading.current_thread().name
        return fn(self, *args, **kwargs)
    return wrapper

