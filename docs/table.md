## Functions

### Book Class

#### Method \_\_init\_\_(self, filename:str="test.xlsx ")

Creates a new instance of the Book class. Accepts one optional argument `filename`, which points to the file name (by default "test.xlsx "). Initializes the Workbook and active sheet objects inside an instance of the Book class. Saves `filename` in the `_filename` field.

#### Method \_sort_date(self, dates:list[str]) -> list[str]

Accepts a list of `dates` strings containing dates in the format "%d.%m.%y". Returns a new list `sorted_dates` containing sorted dates from `dates' in ascending order. Sorting is performed using the function `key=lambda x: mktime(strptime(x, "%d.%m.%y"))`, which converts date strings into a numeric representation and compares them.

#### Method \_get_all_dates(self, data:dict) -> list[str]

Accepts a dictionary `data' representing data with dates. Extracts all dates from `data` and returns a list of `dates` containing all found dates in the format "%d.%m.%y".

#### Method save_xlsx(self, data:dict) -> str

Accepts a dictionary `data' representing data to be written to an Excel file. Writes the header "mac address" to cell 'A1' of the active sheet `_sheet'. Then sorts all the dates from `data` using the `_sort_date()` method. Returns a string with the name of the saved file.