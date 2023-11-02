from time import time, gmtime,\
    strptime, sleep
from threading import Thread
from typing import Callable

class Timer:

    def __init__(self, gap:int=28800, queue:list[Callable]=[]):
        self._gap = gap
        self._queue = queue
        
    def add_to_queue(self, func:Callable=None) -> None:
        if func is None:
            raise Exception("Function is not callable")
        self._queue.append(func)
        
    def remove_from_queue(self, index:int=None) -> None:
        if index is None:
            raise ValueError
        del self._queue[index]
        