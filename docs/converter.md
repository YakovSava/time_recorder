## Converter

The `Converter` class is a tool for converting data using configuration files.

### init(config_file:str='config.ini', compare_list:str='compare.ini')

The 'init` method initializes an object of the `Converter` class.

#### Arguments:

- `config_file' (string): The name of the configuration file (by default "config.ini").
- `compare_list` (string): The name of the file to compare (by default "compare.ini").

### \_read_file(filename:str) -> str

The `_read_file` method reads the contents of the specified file and returns it as a string.

#### Arguments:

- `filename` (string): The name of the file to read.

#### Return value:

- `str`: The contents of the file as a string.

### load_conf() -> dict

The 'load_conf` method loads the contents of the configuration file and returns it as a dictionary.

#### Return value:

- `dict`: The contents of the configuration file in the form of a dictionary.

### \_load_list_compare()

The `_load_list_compare` method loads the contents of the file for comparison and returns it.

#### Return value:

- `dict`: The contents of the file for comparison.

### compare(macs:str=None) -> str

The 'compare` method compares the specified string `macs` using data from the comparison file.

#### Arguments:

- `macs' (string, optional): The string to be compared.

#### Return value:

- `str`: The result of comparing the string `macs` using data from the file for comparison.