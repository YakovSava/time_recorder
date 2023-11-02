from time import time, gmtime,\
    strptime, sleep
from multiprocessing import Process
from typing import Callable

class Timer:

    def __init__(self, gap:int=28800, queue:list[Callable]=[]):
        self._gap = gap
        self._queue = queue
        self._queue_thread:list[Process] = []
        
    def add_to_queue(self, func:Callable=None) -> None:
        if func is None:
            raise Exception("Function is not callable")
        self._queue.append(func)
        
    def remove_from_queue(self, index:int=None) -> None:
        if index is None:
            raise ValueError
        del self._queue[index]

    def _start(self) -> None:
        for func in self._queue:
            self._queue_thread.append(Process(target=func))

        for th in self._queue_thread:
            th.start()

    def _restart(self) -> None:
        for th in self._queue_thread:
            th.terminate()

    def start_job(self) -> bool:
        if all(map(callable, self._queue.copy())):
            pr = Process(target=self._start())
            pr.start()
            return True
        return False