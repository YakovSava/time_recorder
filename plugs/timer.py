from time import time, gmtime,\
    strptime, sleep
from threading import Thread

class Timer:

    def __init__(self, gap:int=28800):
        self._gap = gap