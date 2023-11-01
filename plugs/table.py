from openpyxl import Workbook

class Book:

    def __init__(self, filename:str="test.xlsx"):
        self._book = Workbook()
        self._sheet = self._book.active
        self._filename = filename

    def save_xlsx(self, data:list[list[str, int]]) -> str:
        self._sheet['A1'] = 'mac-адрес'
        self._sheet['B1'] = 'время использования (секунд)'
        for num, item in enumerate(data):
            pass

    def save(self):
        self._book.save(self._filename)
        self._book.close()

    def __del__(self):
        self.save()
        return 1