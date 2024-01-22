from os.path import exists
from time import strftime

class Logger:

    def __init__(self, filename:str='log.log'):
        if not exists(filename):
            mode = 'w+'
        else:
            mode = 'a+'
        self._descriptor = open(filename, mode, encoding='utf-8')

    def read(self) -> str:
        return self._descriptor.read()

    def write(self, data:str) -> None:
        self._descriptor.write(strftime('%d %B %Y %H:%M:%S ->\t')+data)

    def __del__(self):
        self._descriptor.close()