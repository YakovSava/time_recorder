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

