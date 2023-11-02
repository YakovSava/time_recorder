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
        self._stop()

        self._start()

    def start_job(self) -> bool:
        if all(map(callable, self._queue.copy())):
            pr = Process(target=self._start())
            pr.start()
            return True
        return False

    def coro(self, func:Callable, *args, **kwargs) -> Callable:
        def _coro():
            return func(*args, **kwargs)
        return _coro

    def coro_wrapper(self, func:Callable) -> Callable:
        def wrapper(*args, **kwargs):
            def _coro():
                return func(*args, **kwargs)
            return _coro
        return wrapper

    def restart(self) -> bool:
        if all(map(callable, self._queue.copy())):
            pr = Process(target=self._restart())
            pr.start()
            return True
        return False

    def _stop(self):
        for th in self._queue_thread:
            th.terminate()
        self._queue_thread.clear()

    def __del__(self):
        self._stop()
