from toml import loads

class Converter:

    def __init__(self, config_file:str='config.ini', compare_list:str='compare.ini'):
        self._config_filename = config_file
        self._compare_file = compare_list

    def _read_file(self, filename:str) -> str:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

    def load_conf(self) -> dict:
        return loads(self._read_file(self._config_filename))

    def _load_list_compare(self):
        return loads(self._read_file(self._compare_file))

    def compare(self, macs:str=None) -> str:
        if not macs:
            raise
        for _from, _to in self._load_list_compare()['compare']: macs = macs.replace(_from ,_to)
        return macs