from warnings import warn

warn("'That's tested session getter")

class Getter:

    def __init__(self, address:str=None):
        if address is None:
            self._file_mode = True
        else:
            self._file_mode = False

        self._address = address
        self._filename = 'test.csv'
        self._database_filename = 'table_raw.csv'

    def _load(self) -> list[list[str, int]]:
        with open(self._filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return list(map(lambda x: x.split(';'), lines))

    def _parse_site(self) -> str:
        return ""

    def parse_sessions(self) -> list[list[str, int]]:
        if self._file_mode:
            return self._load()
        else:
            return self._parse_site()

