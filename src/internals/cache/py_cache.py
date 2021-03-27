from threading import Lock
import datetime

from ...utils.utils import get_value

cache = None

def init():
    global cache
    cache = PyCache()

def get_cache():
    global cache
    return cache

class PyCache():

    def __init__(self):
        self.cache = dict()
        self.lock = Lock()

    def set(self, key, value, ex = None):
        if ex is not None:
            ex = datetime.datetime.now() + datetime.timedelta(seconds=ex)

        self.lock.acquire()
        try:
            self.cache[key] = {
                'value': value,
                'expire': ex
            }
        finally:
            self.lock.release()

    def get(self, key):
        self.lock.acquire()
        try:
            entry = get_value(self.cache, key)
            if entry is None:
                return None

            if entry['expire'] is not None:
                if entry['expire'] < datetime.datetime.now():
                    del self.cache[key]
                    return None

            return self.cache[key]['value']
        finally:
            self.lock.release()

    def delete(self, key):
        self.lock.acquire()
        try:
            if key in self.cache:
                del self.cache[key]
        finally:
            self.lock.release()
