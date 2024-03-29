from time import strptime, mktime, strftime
from openpyxl import Workbook
from .converter import Converter

excel_alphabet = [chr(i) for i in range(65, 91)]
for it in [[chr(j) + chr(i) for i in range(65, 91)] for j in range(65, 91)]:
    excel_alphabet.extend(it)


class Book:

    def __init__(self, filename: str="test.xlsx", cmp: Converter=None):
        self._book = Workbook()
        self._sheet = self._book.active
        self._filename = filename
        self._cmp = cmp

    def _sort_date(self, dates: list[str]) -> list[str]:
        return sorted(dates, key=lambda x: mktime(strptime(x, "%d.%m.%y")))

    def _get_all_dates(self, data: dict) -> list[str]:
        dates = []
        for value in data.values():
            for date in value.keys():
                dates.append(date)
        return dates

    def save_xlsx(self, data: dict) -> str:
        # print(data)
        self._sheet['A1'] = 'mac-адрес'
        dates = self._sort_date(self._get_all_dates(data))
        used_dates = []
        counter = 0
        for date in dates:
            if date not in used_dates:
                self._sheet[f'{excel_alphabet[counter+1]}1'] = date
                used_dates.append(date)
                counter += 1
        for i, mac in enumerate(data.keys(), start=1):
            self._sheet[f'A{i+1}'] = self._cmp.compare(mac)
            # print(data)
            for j, date in enumerate(used_dates, start=1):
                try:
                    self._sheet[f'{excel_alphabet[j]}{i+1}'] = data[mac][date]
                except Exception as ex:
                    self._sheet[f'{excel_alphabet[j]}{i+1}'] = 0
        self.save(self._filename)

        return self._filename

    def save(self, filename: str=...):
        try:
            self._book.save(filename)
            self._book.close()
        except:
            pass

    def __del__(self):
        self.save()
        return 1
