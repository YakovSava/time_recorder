
# Класс Book для работы с книгами Excel

Класс Book предназначен для создания и сохранения электронных таблиц в формате Excel.

**Атрибуты:**

* `_book` (Workbook): Объект класса Workbook из библиотеки openpyxl, представляющий книгу Excel.
* `_sheet` (Worksheet): Объект класса Worksheet из библиотеки openpyxl, представляющий активный лист книги.
* `_filename` (str): Имя файла книги Excel.
* `_cmp` (Converter): Объект класса Converter (необязательный), используемый для преобразования данных перед сохранением в книгу.

**Методы:**

* `__init__(self, filename: str="test.xlsx", cmp: Converter=None)`: Инициализирует экземпляр класса.
* `_sort_date(self, dates: list[str]) -> list[str]`: Сортирует список дат по возрастанию.
* `_get_all_dates(self, data: dict) -> list[str]`: Извлекает все уникальные даты из данных.
* `save_xlsx(self, data: dict) -> str`: Сохраняет данные в книгу Excel.
    * Принимает словарь данных, где ключами являются MAC-адреса, а значениями - словари с датами в качестве ключей и значениями данных для соответствующих дат.
    * Возвращает имя сохраненного файла.
* `save(self, filename: str=...)`: Сохраняет книгу Excel.
* `__del__(self)`: Деструктор класса, автоматически сохраняет книгу при удалении объекта.

**Пример использования:**

```python
from converter import MyConverter  # Импорт класса Converter

data = {"AA:BB:CC:DD:EE:FF": {"20.02.2024": "Value 1", "21.02.2024": "Value 2"}}
book = Book("report.xlsx", MyConverter())
book.save_xlsx(data)
