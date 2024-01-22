from os.path import exists
from time import strftime

class Logger:

    def __init__(self, filename:str='log.log'):
        if not exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('')
        self._descriptor = open(filename, 'a+', encoding='utf-8')

    def read(self) -> str:
        return self._descriptor.read()

    def write(self, data:str) -> None:
        self._descriptor.write(strftime('%d %B %Y %H:%M:%S ->\t')+data+'\n')

    def __del__(self):
        self._descriptor.close()