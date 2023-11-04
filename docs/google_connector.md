## Class GDrive

The `GDrive` class provides methods for working with Google Drive.

### The `init()` method

Initializes the 'GDrive` object and creates an instance of `Google Drive` for further work with Google Drive.

#### Arguments

This method does not accept arguments.

#### Return value

This method does not return values.

### Method `send_exc_file(filename:str="table.xlsx ") -> bool`

Sends the file to Google Drive.

#### Arguments

- `filename` (type: `str', default: `"table.xlsx "`): The name of the file to be sent to Google Drive. If the argument value is not specified, the default file name will be used.

#### Return value

Type: `bool`

When the file is successfully uploaded to Google Drive, the function returns `True`. Otherwise, `False'.