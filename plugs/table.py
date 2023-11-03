from time import strptime, mktime
from openpyxl import Workbook

excel_alphabet = [chr(i) for i in range(65, 91)]
for it in [[chr(j)+chr(i) for i in range(65, 91)] for j in range(65, 91)]:
    excel_alphabet.extend(it)

class Book:

    def __init__(self, filename:str="test.xlsx"):
        self._book = Workbook()
        self._sheet = self._book.active
        self._filename = filename

    def _sort_date(self, dates:list[str]) -> list[str]:
        return sorted(dates, key=lambda x: mktime(strptime(x, "%d.%m.%y")))

    def _get_all_dates(self, data:dict) -> list[str]:
        dates = []
        for value in data.values():
            for date in value.keys():
                dates.append(date)
        return dates

    def save_xlsx(self, data:dict) -> str:
        self._sheet['A1'] = 'mac-адрес'
        dates = self._sort_date(self._get_all_dates(data))
        for i, data in enumerate(data.items()):
            self._sheet[f'{excel_alphabet[i+1]}{i}'] = ...
        self.save()

        return self._filename

    def save(self):
        self._book.save(self._filename)
        self._book.close()

    def __del__(self):
        self.save()
        return 1