
# Класс Getter для парсинга логов о подключениях устройств по Wi-Fi

Этот класс предназначен для извлечения и анализа информации о подключениях устройств по Wi-Fi из файлов журналов.

**Атрибуты:**

* `_filename` (str): Имя файла журнала для парсинга.
* `_tested` (bool): Флаг, указывающий на использование тестового файла журнала.
* `_test_filename` (str): Имя тестового файла журнала.
* `_pattern` (re.compile): Регулярное выражение для поиска строк, начинающихся с "".

**Методы:**

* `__init__(self, filename=None, tested=False)`: Инициализирует экземпляр класса.
* `_get_STA(self, line: str) -> str`: Извлекает MAC-адрес клиента из строки журнала.
* `_is_mac_address(self, string: str) -> bool`: Проверяет, является ли строка действительным MAC-адресом.
* `extract_mac_address(self, text: str) -> str`: Извлекает MAC-адрес из текста.
* `_format_system_log(self, line: str) -> str`: Форматирует строку журнала системы.
* `parse_file(self) -> dict`: Парсит файл журнала и возвращает словарь с информацией о подключениях устройств.
* `calculate_times(self, parsed_log: dict) -> dict`: Анализирует информацию о подключениях и возвращает словарь с суммарным временем подключения для каждого устройства по каждому дню.

**Пример использования:**

```python
getter = Getter("wpa_supplicant.log")
parsed_data = getter.parse_file()
result = getter.calculate_times(parsed_data)
print(result)
