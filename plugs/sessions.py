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
            raise NotImplemented

    def _update(self, a:list[list[str, int]], b:list[list[str, int]]):
        for item_b in b:
            found = False
            for i, item_a in enumerate(a):
                if item_b[0] == item_a[0]:
                    a[i][1] = item_b[1]
                    found = True
                    break
            if not found:
                a.append(item_b)
        return a

    def reload(self) -> list[list[str, int]]:
        updates = self._update(self.get_db(), self.parse_sessions())
        self.save(updates)
        return updates

    def save(self, data:list[list[str, int]]) -> None:
        with open(self._database_filename, 'w', encoding='utf-8') as file:
            to_write = ''
            for mac, seconds in data:
                to_write += f'{mac};{seconds}\n'
            file.write(to_write)

    def get_db(self) -> list[list[str, int]]:
        with open(self._database_filename, 'r', encoding='utf-8') as file:
            lines = map(lambda x: [x[0], eval(x[1])], map(lambda x: x.split(';'), file.readlines()))
        return list(lines)