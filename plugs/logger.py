from os.path import exists
from time import strftime

class Logger:

    def __init__(self, filename:str='log.log', debug:bool=False):
        if not exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('')
        self._descriptor = open(filename, 'a+', encoding='utf-8')
        self._debug = debug

    def read(self) -> str:
        return self._descriptor.read()

    def write(self, data:str) -> None:
        if self._debug:
            print(strftime('%d %B %Y %H:%M:%S ->\t')+data)
        self._descriptor.write(strftime('%d %B %Y %H:%M:%S ->\t')+data+'\n')

    def __del__(self):
        self._descriptor.close()